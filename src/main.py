#!/usr/bin/env python3
"""
Basketball Analytics Research Agent
A LangChain agent that can research basketball statistics and analytics from basketball-reference.com
"""

import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain.memory import ConversationBufferMemory

class BasketballReferenceToolkit:
    """Tools for scraping basketball data from basketball-reference.com"""
    
    def __init__(self):
        self.base_url = "https://www.basketball-reference.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_player(self, player_name: str) -> str:
        """Search for a player and return their basic info and stats"""
        try:
            # Format player name for URL (first letter of first name + last name)
            name_parts = player_name.strip().split()
            if len(name_parts) < 2:
                return f"Please provide both first and last name for {player_name}"
            
            first_initial = name_parts[0][0].lower()
            last_name = name_parts[-1].lower()
            
            # Try common URL pattern
            player_url = f"{self.base_url}/players/{last_name[0]}/{last_name[:5]}{first_initial}01.html"
            
            response = requests.get(player_url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract player info
                player_info = []
                
                # Get player name and basic info
                name_elem = soup.find('h1')
                if name_elem:
                    player_info.append(f"Player: {name_elem.get_text(strip=True)}")
                
                # Get career stats table
                stats_table = soup.find('table', {'id': 'per_game'})
                if stats_table:
                    rows = stats_table.find_all('tr')
                    if len(rows) > 1:  # Skip header
                        # Get career totals (usually last row)
                        career_row = None
                        for row in rows:
                            if 'Career' in row.get_text():
                                career_row = row
                                break
                        
                        if career_row:
                            cells = career_row.find_all(['td', 'th'])
                            if len(cells) > 10:
                                player_info.append(f"Career PPG: {cells[29].get_text(strip=True) if len(cells) > 29 else 'N/A'}")
                                player_info.append(f"Career RPG: {cells[23].get_text(strip=True) if len(cells) > 23 else 'N/A'}")
                                player_info.append(f"Career APG: {cells[24].get_text(strip=True) if len(cells) > 24 else 'N/A'}")
                
                return "\n".join(player_info) if player_info else "Player found but stats not available"
            else:
                return f"Player {player_name} not found. Try a different spelling or check if they played in the NBA."
                
        except Exception as e:
            return f"Error searching for {player_name}: {str(e)}"
    
    def get_team_stats(self, team_abbrev: str, year: str = "2024") -> str:
        """Get team statistics for a given year"""
        try:
            team_url = f"{self.base_url}/teams/{team_abbrev.upper()}/{year}.html"
            response = requests.get(team_url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                team_info = []
                
                # Get team name
                title = soup.find('title')
                if title:
                    team_info.append(f"Team: {title.get_text().split('|')[0].strip()}")
                
                # Get basic team stats
                team_stats_table = soup.find('table', {'id': 'team_stats'})
                if team_stats_table:
                    rows = team_stats_table.find_all('tr')
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) > 1:
                            stat_name = cells[0].get_text(strip=True)
                            stat_value = cells[1].get_text(strip=True)
                            if stat_name in ['Points', 'Field Goals', 'Rebounds', 'Assists']:
                                team_info.append(f"{stat_name}: {stat_value}")
                
                return "\n".join(team_info) if team_info else "Team stats not found"
            else:
                return f"Team {team_abbrev} not found for {year}. Check team abbreviation and year."
                
        except Exception as e:
            return f"Error getting team stats: {str(e)}"
    
    def get_league_leaders(self, stat_type: str = "pts", year: str = "2024") -> str:
        """Get league leaders for a specific statistic"""
        try:
            leaders_url = f"{self.base_url}/leagues/NBA_{year}_leaders.html"
            response = requests.get(leaders_url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find the appropriate stats table
                stats_tables = soup.find_all('table')
                leaders_info = []
                
                for table in stats_tables[:3]:  # Check first few tables
                    if table:
                        rows = table.find_all('tr')[:6]  # Get top 5 leaders
                        for i, row in enumerate(rows[1:], 1):  # Skip header
                            cells = row.find_all(['td', 'th'])
                            if len(cells) >= 3:
                                player = cells[0].get_text(strip=True)
                                value = cells[1].get_text(strip=True)
                                leaders_info.append(f"{i}. {player}: {value}")
                        if leaders_info:
                            break
                
                return f"League Leaders ({year}):\n" + "\n".join(leaders_info) if leaders_info else "League leaders not found"
            else:
                return f"Could not fetch league leaders for {year}"
                
        except Exception as e:
            return f"Error getting league leaders: {str(e)}"

def create_basketball_agent():
    """Create and configure the basketball analytics research agent"""
    
    # Load environment variables
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
    
    # Initialize LLM
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    
    # Initialize basketball reference toolkit
    bb_toolkit = BasketballReferenceToolkit()
    
    # Create tools
    tools = [
        Tool(
            name="search_player",
            description="Search for NBA player statistics and information. Input should be the player's full name (first and last name).",
            func=bb_toolkit.search_player
        ),
        Tool(
            name="get_team_stats",
            description="Get team statistics for a specific year. Input should be team abbreviation and year (optional, defaults to 2024). Example: 'LAL 2023'",
            func=lambda x: bb_toolkit.get_team_stats(*x.split()) if ' ' in x else bb_toolkit.get_team_stats(x)
        ),
        Tool(
            name="get_league_leaders",
            description="Get league leaders for various statistics. Input can be stat type and year. Example: 'pts 2023'",
            func=lambda x: bb_toolkit.get_league_leaders(*x.split()) if ' ' in x else bb_toolkit.get_league_leaders(x)
        )
    ]
    
    # Create agent prompt
    prompt = PromptTemplate.from_template("""
You are a basketball analytics research assistant with access to basketball-reference.com data.
You can help users find player statistics, team performance data, and league leaders.

Available tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought: {agent_scratchpad}
""")
    
    # Create agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )
    
    return agent_executor

def main():
    """Main function to run the basketball analytics agent"""
    print("🏀 Basketball Analytics Research Agent")
    print("Ask me about NBA players, teams, or league statistics!\n")
    
    # Create agent
    agent = create_basketball_agent()
    
    # Test queries for demonstration
    test_queries = [
        "Tell me about LeBron James career statistics",
        "What are the Lakers team stats for 2024?",
        "Who are the league leaders in scoring?"
    ]
    
    # Run test queries
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        print("=" * 50)
        
        try:
            response = agent.invoke({"input": query})
            print(f"📊 Answer: {response['output']}\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
    
    print("\n✅ Basketball Analytics Agent is ready!")
    print("To use interactively, modify the main() function to include the input loop.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Animal Research Agent with LangGraph
Comprehensive animal research and reporting using web search and AI analysis
"""

import os
import sys
from typing import Dict, List, Any, TypedDict
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.tools import Tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

class AnimalResearcher:
    """Animal research assistant using web search and AI analysis"""
    
    def __init__(self):
        # Load environment variables for web search
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
        
    def search_basic_info(self, animal: str) -> str:
        """Search for basic information about an animal"""
        prompt = f"""Provide basic information about {animal}, including:
        - Scientific name and classification
        - Physical description and size
        - Basic habitat information
        - Diet type (carnivore, herbivore, omnivore)
        - Lifespan
        
        Be factual and concise."""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    def research_habitat_distribution(self, animal: str) -> str:
        """Research habitat and geographic distribution"""
        prompt = f"""Research the habitat and geographic distribution of {animal}:
        - Current geographic range and distribution
        - Preferred habitats and ecosystems
        - Migration patterns (if applicable)
        - Historical vs current range changes
        - Climate and environmental requirements
        
        Provide detailed, factual information."""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    def research_behavior_social_structure(self, animal: str) -> str:
        """Research behavior and social structure"""
        prompt = f"""Research the behavior and social structure of {animal}:
        - Social organization and group dynamics
        - Mating and reproductive behavior
        - Communication methods
        - Hunting/feeding behaviors
        - Parental care and offspring development
        - Notable behavioral adaptations
        
        Provide comprehensive behavioral insights."""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    def research_conservation_status(self, animal: str) -> str:
        """Research conservation status and threats"""
        prompt = f"""Research the conservation status and threats facing {animal}:
        - Current IUCN Red List status
        - Population trends and estimates
        - Major threats (habitat loss, climate change, hunting, etc.)
        - Conservation efforts and programs
        - Success stories or ongoing challenges
        - Future outlook
        
        Focus on current, factual conservation information."""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    def research_evolutionary_history(self, animal: str) -> str:
        """Research evolutionary history and relationships"""
        prompt = f"""Research the evolutionary history of {animal}:
        - Evolutionary origins and timeline
        - Fossil record and prehistoric relatives
        - Key evolutionary adaptations
        - Closest living relatives
        - Phylogenetic relationships
        - Interesting evolutionary facts
        
        Provide scientifically accurate evolutionary information."""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content

class ResearchState(TypedDict):
    """State for the animal research LangGraph workflow"""
    messages: List[Any]
    animal: str
    research_sections: Dict[str, str]
    final_report: str

def create_animal_research_workflow():
    """Create a LangGraph workflow for comprehensive animal research"""
    
    # Initialize researcher
    researcher = AnimalResearcher()
    
    def extract_animal_name(state: ResearchState) -> ResearchState:
        """Extract animal name from the user's query"""
        query = state["messages"][-1].content.lower()
        
        # Look for patterns like "research [animal]" or "tell me about [animal]"
        animal_name = ""
        
        # Remove common research phrases to isolate animal name
        query_clean = query.replace("research", "").replace("tell me about", "").replace("information about", "")
        query_clean = query_clean.replace("study", "").replace("analyze", "").strip()
        
        # Capitalize first letter of each word for proper animal names
        animal_name = query_clean.title()
        
        state["animal"] = animal_name
        state["research_sections"] = {}
        
        return state
    
    def research_basic_info_node(state: ResearchState) -> ResearchState:
        """Research basic information about the animal"""
        animal = state["animal"]
        basic_info = researcher.search_basic_info(animal)
        state["research_sections"]["basic_info"] = basic_info
        return state
    
    def research_habitat_node(state: ResearchState) -> ResearchState:
        """Research habitat and distribution"""
        animal = state["animal"]
        habitat_info = researcher.research_habitat_distribution(animal)
        state["research_sections"]["habitat"] = habitat_info
        return state
    
    def research_behavior_node(state: ResearchState) -> ResearchState:
        """Research behavior and social structure"""
        animal = state["animal"]
        behavior_info = researcher.research_behavior_social_structure(animal)
        state["research_sections"]["behavior"] = behavior_info
        return state
    
    def research_conservation_node(state: ResearchState) -> ResearchState:
        """Research conservation status"""
        animal = state["animal"]
        conservation_info = researcher.research_conservation_status(animal)
        state["research_sections"]["conservation"] = conservation_info
        return state
    
    def research_evolution_node(state: ResearchState) -> ResearchState:
        """Research evolutionary history"""
        animal = state["animal"]
        evolution_info = researcher.research_evolutionary_history(animal)
        state["research_sections"]["evolution"] = evolution_info
        return state
    
    def synthesize_report(state: ResearchState) -> ResearchState:
        """Synthesize all research into a comprehensive report"""
        animal = state["animal"]
        sections = state["research_sections"]
        
        # Create comprehensive report
        report = f"""# Comprehensive Research Report: {animal}

## 1. Basic Information and Classification
{sections.get('basic_info', 'Information not available')}

## 2. Habitat and Geographic Distribution  
{sections.get('habitat', 'Information not available')}

## 3. Behavior and Social Structure
{sections.get('behavior', 'Information not available')}

## 4. Conservation Status and Threats
{sections.get('conservation', 'Information not available')}

## 5. Evolutionary History and Relationships
{sections.get('evolution', 'Information not available')}

---
*This comprehensive report was generated through systematic research across multiple domains of knowledge about {animal}.*
"""
        
        state["final_report"] = report
        state["messages"].append(AIMessage(content=report))
        
        return state
    
    # Build the workflow graph
    workflow = StateGraph(ResearchState)
    
    # Add research nodes
    workflow.add_node("extract_animal", extract_animal_name)
    workflow.add_node("basic_info", research_basic_info_node)
    workflow.add_node("habitat", research_habitat_node) 
    workflow.add_node("behavior", research_behavior_node)
    workflow.add_node("conservation", research_conservation_node)
    workflow.add_node("evolution", research_evolution_node)
    workflow.add_node("synthesize", synthesize_report)
    
    # Define the research pipeline
    workflow.set_entry_point("extract_animal")
    workflow.add_edge("extract_animal", "basic_info")
    workflow.add_edge("basic_info", "habitat")
    workflow.add_edge("habitat", "behavior") 
    workflow.add_edge("behavior", "conservation")
    workflow.add_edge("conservation", "evolution")
    workflow.add_edge("evolution", "synthesize")
    workflow.add_edge("synthesize", END)
    
    return workflow.compile()

def main():
    """Main function to run the animal research agent"""
    print("🔬 Animal Research Agent with LangGraph")
    print("Comprehensive animal research and reporting!\n")
    
    # Check for command line argument
    if len(sys.argv) != 2:
        print("Usage: python main.py [animal_name]")
        print("Example: python main.py orcas")
        print("Example: python main.py 'polar bears'")
        sys.exit(1)
    
    # Get animal name from command line argument
    animal_name = sys.argv[1]
    query = f"Research {animal_name}"
    
    print(f"🔍 Researching: {animal_name}")
    print("=" * 60)
    
    # Create research workflow
    workflow = create_animal_research_workflow()
    
    try:
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "animal": "",
            "research_sections": {},
            "final_report": ""
        }
        
        print("🔄 Starting comprehensive research workflow...")
        print("📊 Gathering information across multiple domains...")
        
        # Run the research workflow
        result = workflow.invoke(initial_state)
        
        # Print the comprehensive report
        print("\n📋 COMPREHENSIVE RESEARCH REPORT:")
        print(result["final_report"])
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
    
    print(f"\n✅ Research on {animal_name} completed successfully!")
    print("Report generated with:")
    print("- Basic information and classification")
    print("- Habitat and geographic distribution")
    print("- Behavior and social structure")
    print("- Conservation status and threats")
    print("- Evolutionary history and relationships")

if __name__ == "__main__":
    main()
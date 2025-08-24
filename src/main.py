#!/usr/bin/env python3
"""
LangChain Hello World - 4 Key Steps
"""

from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

def main():
    # 1. Load environment variables
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
    
    # 2. Initialize LLM
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    
    # 3. Create prompt template
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Tell me one interesting fact about {topic}"
    )
    
    # 4. Run the chain
    chain = prompt | llm
    result = chain.invoke({"topic": "AI"})
    
    print(result.content)

if __name__ == "__main__":
    main()
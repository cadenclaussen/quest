#!/usr/bin/env python3
"""
Hello World LangChain Application

A simple demonstration of LangChain basics including:
- LLM initialization
- Prompt templates
- Chain creation
- Basic conversation
"""

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    """Main function demonstrating LangChain hello world."""
    
    print("🦜 LangChain Hello World Application")
    print("=" * 40)
    
    # Initialize OpenAI LLM (requires OPENAI_API_KEY in environment)
    try:
        llm = OpenAI(
            temperature=0.7,
            max_tokens=100
        )
        print("✅ LLM initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize LLM: {e}")
        print("💡 Make sure to set OPENAI_API_KEY in your environment")
        return
    
    # Create a simple prompt template
    prompt_template = PromptTemplate(
        input_variables=["name"],
        template="Hello {name}! Please tell me an interesting fact about artificial intelligence."
    )
    
    # Create an LLM chain
    chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=True
    )
    
    # Run the chain
    try:
        name = "World"
        print(f"\n🔄 Running chain with input: {name}")
        
        result = chain.run(name=name)
        
        print(f"\n🤖 AI Response:")
        print("-" * 20)
        print(result.strip())
        print("-" * 20)
        
    except Exception as e:
        print(f"❌ Error running chain: {e}")
        return
    
    print("\n✨ LangChain Hello World completed successfully!")

if __name__ == "__main__":
    main()
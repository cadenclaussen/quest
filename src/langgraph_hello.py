#!/usr/bin/env python3
"""
LangGraph Hello World - Simple State Graph Example
"""

from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from typing import TypedDict
from dotenv import load_dotenv
import os


class GraphState(TypedDict):
    """State of the graph"""
    message: str
    processed: bool


def greeting_node(state: GraphState) -> GraphState:
    """Node that generates a greeting"""
    return {
        "message": "Hello from LangGraph!",
        "processed": False
    }


def processing_node(state: GraphState) -> GraphState:
    """Node that processes the greeting with Claude"""
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
    
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    
    enhanced_message = llm.invoke(
        f"Make this greeting more enthusiastic and add an interesting fact about graphs: {state['message']}"
    )
    
    return {
        "message": enhanced_message.content,
        "processed": True
    }


def should_continue(state: GraphState) -> str:
    """Conditional edge function"""
    if state["processed"]:
        return "__end__"
    return "process"


def main():
    """Main function to run the LangGraph hello world"""
    
    # Create the state graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("greeting", greeting_node)
    workflow.add_node("process", processing_node)
    
    # Set entry point
    workflow.set_entry_point("greeting")
    
    # Add edges
    workflow.add_conditional_edges(
        "greeting",
        lambda x: "process",  # Always go to process from greeting
        {"process": "process"}
    )
    
    workflow.add_conditional_edges(
        "process",
        should_continue,
        {"__end__": END}
    )
    
    # Compile the graph
    app = workflow.compile()
    
    # Run the graph
    initial_state = {"message": "", "processed": False}
    final_state = app.invoke(initial_state)
    
    print("=== LangGraph Hello World Result ===")
    print(final_state["message"])
    print("=====================================")


if __name__ == "__main__":
    main()
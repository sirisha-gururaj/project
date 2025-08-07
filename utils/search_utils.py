import os
from langchain_community.tools.tavily_search import TavilySearchResults
import sys
import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config

# Set the Tavily API key as an environment variable for the tool
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

def perform_web_search(query: str):
    """
    Performs a real-time web search using the Tavily API.
    """
    print(f"Performing web search for: {query}")
    try:
        # k=3 means it will return the top 3 search results
        search_tool = TavilySearchResults(k=3)
        results = search_tool.invoke({"query": query})

        # Format the results into a single string for the context
        formatted_results = "\n\n".join([res["content"] for res in results])
        return formatted_results
    except Exception as e:
        print(f"Error during web search: {e}")
        return "Sorry, the web search failed. Please check the API key and network connection."
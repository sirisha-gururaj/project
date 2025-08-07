import os
import sys
from langchain_groq import ChatGroq
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import config
import streamlit as st
def get_chatgroq_model():
    """Initialize and return the Groq chat model"""
    try:
        # Initialize the Groq chat model with the API key
        groq_model = ChatGroq(
            groq_api_key=st.secrets["GROQ_API_KEY"],
            model_name="llama-3.1-8b-instant",
        )
        return groq_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")
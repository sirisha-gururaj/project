import streamlit as st
import os
import sys
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all necessary components
from models.llm import get_chatgroq_model
from config import config
from utils.rag_utils import setup_rag_pipeline, query_rag_pipeline
from utils.search_utils import perform_web_search


def get_chat_response(chat_model, messages, system_prompt):
    """Get response from the chat model"""
    try:
        formatted_messages = [SystemMessage(content=system_prompt)]
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
        
        response = chat_model.invoke(formatted_messages)
        return response.content
    
    except Exception as e:
        st.error(f"Error communicating with the AI model: {e}")
        return "Sorry, I encountered an error. Please try again."

def instructions_page():
    """Instructions and setup page"""
    st.title("The Chatbot Blueprint")
    st.markdown("Welcome! Follow these instructions to set up and use the chatbot.")
    
    st.markdown("""
    ## 🔧 Installation
                
    
    First, install the required dependencies: (Add Additional Libraries base don your needs)
    
    ```bash
    pip install -r requirements.txt
    ```
    
    ## API Key Setup
    
    You'll need API keys from your chosen provider. Get them from:
    
    ### OpenAI
    - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
    - Create a new API key
    - Set the variables in config
    
    ### Groq
    - Visit [Groq Console](https://console.groq.com/keys)
    - Create a new API key
    - Set the variables in config
    
    ### Google Gemini
    - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
    - Create a new API key
    - Set the variables in config
    
    ## 📝 Available Models
    
    ### OpenAI Models
    Check [OpenAI Models Documentation](https://platform.openai.com/docs/models) for the latest available models.
    Popular models include:
    - `gpt-4o` - Latest GPT-4 Omni model
    - `gpt-4o-mini` - Faster, cost-effective version
    - `gpt-3.5-turbo` - Fast and affordable
    
    ### Groq Models
    Check [Groq Models Documentation](https://console.groq.com/docs/models) for available models.
    Popular models include:
    - `llama-3.1-70b-versatile` - Large, powerful model
    - `llama-3.1-8b-instant` - Fast, smaller model
    - `mixtral-8x7b-32768` - Good balance of speed and capability
    
    ### Google Gemini Models
    Check [Gemini Models Documentation](https://ai.google.dev/gemini-api/docs/models/gemini) for available models.
    Popular models include:
    - `gemini-1.5-pro` - Most capable model
    - `gemini-1.5-flash` - Fast and efficient
    - `gemini-pro` - Standard model
    
    ## How to Use
    
    1. **Go to the Chat page** (use the navigation in the sidebar)
    2. **Start chatting** once everything is configured!
    
    ## Tips
    
    - **System Prompts**: Customize the AI's personality and behavior
    - **Model Selection**: Different models have different capabilities and costs
    - **API Keys**: Can be entered in the app or set as environment variables
    - **Chat History**: Persists during your session but resets when you refresh
    
    ## Troubleshooting
    
    - **API Key Issues**: Make sure your API key is valid and has sufficient credits
    - **Model Not Found**: Check the provider's documentation for correct model names
    - **Connection Errors**: Verify your internet connection and API service status
    
    ---
    
    Ready to start chatting? Navigate to the **Chat** page using the sidebar! 
    """)

def chat_page(response_mode: str):
    """Main chat interface page"""
    st.title("🤖 MyCampusBot")

    @st.cache_resource(show_spinner="Loading campus knowledge...")
    def load_retriever():
        return setup_rag_pipeline()

    retriever = load_retriever()
    
    # This is the general instruction for the AI's personality.
    system_prompt = "You are a helpful and friendly Student Helpdesk assistant for the Global University of Innovation. Your main role is to answer student queries accurately based on the context provided to you."

    chat_model = get_chatgroq_model()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Get user input from the chat box
    if prompt := st.chat_input("Ask about campus or anything else..."):
        # When user types a new message, add it to history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # This block automatically generates a response if the last message is from the user
    # It also handles re-generating a response when the response_mode is changed
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                last_user_prompt = st.session_state.messages[-1]["content"]

                # --- RAG + Web Search Fallback Logic ---
                relevant_docs = query_rag_pipeline(retriever, last_user_prompt)
                
                if relevant_docs:
                    st.info("Found relevant information in campus documents...")
                    context = "\n\n".join([doc.page_content for doc in relevant_docs])
                    source_type = "campus documents"
                else:
                    st.info("Couldn't find an answer in campus documents, searching the web...")
                    context = perform_web_search(last_user_prompt)
                    source_type = "web search results"
                # --- End of Fallback Logic ---

                # --- Response Mode Logic ---
                if response_mode == "Concise":
                    style_note = "Provide a concise summary of the answer, not exceeding 3 sentences."
                else: # Detailed
                    style_note = "Provide a comprehensive, detailed answer. Use bullet points for lists if it improves clarity."
                # --- End of Response Mode Logic ---

                # Create the final, fully detailed prompt for the LLM
                final_prompt = f"""Based on the following context from {source_type}, {style_note}

                Context:
                {context}

                User Question:
                {last_user_prompt}
                """
                
                # We don't include the full history for this turn to keep the context clean
                response = get_chat_response(chat_model, [{"role": "user", "content": final_prompt}], system_prompt)
                st.markdown(response)

        # Add the assistant's response to the message history
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    """Main function to run the Streamlit app"""
    st.set_page_config(
        page_title="MyCampusBot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to:", ["Chat", "Instructions"], index=0)
        
        st.divider()
        st.title("Settings")
        response_mode = st.radio(
            "Response Mode", 
            ("Detailed", "Concise"),
            help="Select 'Detailed' for in-depth answers or 'Concise' for short, summarized replies."
        )

        # Your logic to automatically re-ask the last question when the mode is changed
        if "last_response_mode" not in st.session_state:
            st.session_state.last_response_mode = response_mode
        elif st.session_state.last_response_mode != response_mode:
            st.session_state.last_response_mode = response_mode
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
                # Find the last user message to re-ask
                for msg in reversed(st.session_state.messages):
                    if msg["role"] == "user":
                        st.session_state.messages.append({"role": "user", "content": msg["content"]})
                        st.rerun()
                        break
        
        if page == "Chat":
            st.divider()
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    
    if page == "Instructions":
        instructions_page()
    elif page == "Chat":
        chat_page(response_mode=response_mode)

if __name__ == "__main__":
    main()


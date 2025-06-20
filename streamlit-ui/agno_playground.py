import streamlit as st
from agno.agent import Agent
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.vectordb.mongodb import MongoDb
from agno.models.ollama import Ollama
from agno.embedder.ollama import OllamaEmbedder
import dotenv
import os
import time

# Load environment variables from parent directory
dotenv.load_dotenv("../.env")

# Page configuration
st.set_page_config(
    page_title="SF GURU", page_icon="🤖", layout="wide"
)

# Title and description
st.title("SF GURU")
st.markdown(
    """
SF GURU (Generate Understanding from Resource URLs) allows you to create an AI agent with knowledge from any website. 
Simply input a URL, and the agent will learn from that website's content!
"""
)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # URL input
    url = st.text_input(
        "Enter Website URL",
        placeholder="https://example.com",
        help="Enter the URL of the website you want the agent to learn from",
    )

    # Max links configuration
    max_links = st.slider(
        "Maximum Links to Crawl",
        min_value=1,
        max_value=50,
        value=10,
        help="Number of links to crawl from the main URL",
    )

    # Model selection
    model_id = st.selectbox(
        "Select Ollama Model",
        ["llama3.1", "llama3.2", "llama3.2-vision", "openhermes", "mistral"],
        help="Choose the Ollama model to use for the agent",
    )

    # Collection name
    collection_name = st.text_input(
        "Knowledge Base Collection Name",
        value="playground_knowledge",
        help="Name for the MongoDB collection to store the knowledge base",
    )

# Main content area
if url:
    if st.button("🚀 Initialize Agent with Knowledge Base", type="primary"):
        try:
            with st.spinner("Setting up the agent..."):
                # Initialize vector database
                vector_db = MongoDb(
                    collection_name=collection_name,
                    db_url=os.getenv("mdb_url"),
                    embedder=OllamaEmbedder(id="openhermes"),
                )

                # Create knowledge base
                knowledge_base = WebsiteKnowledgeBase(
                    urls=[url], max_links=max_links, vector_db=vector_db
                )

                # Create agent
                agent = Agent(
                    model=Ollama(id=model_id),
                    knowledge=knowledge_base,
                    markdown=True,
                )

                # Load knowledge base
                with st.status("Loading knowledge base...", expanded=True) as status:
                    st.write(f"Crawling {url} and up to {max_links} links...")
                    agent.knowledge.load(recreate=True)
                    status.update(
                        label="Knowledge base loaded successfully!", state="complete"
                    )

                # Store agent in session state
                st.session_state.agent = agent
                st.session_state.knowledge_loaded = True
                st.session_state.url = url

                st.success(f"✅ Agent initialized with knowledge from {url}")

        except Exception as e:
            st.error(f"❌ Error initializing agent: {str(e)}")
            st.error(
                "Make sure your MongoDB URL is set in the .env file and Ollama is running."
            )

# Chat interface
if st.session_state.get("knowledge_loaded", False):
    st.divider()
    st.header("💬 Chat with Your Knowledge Base")
    st.info(
        f"Agent is ready with knowledge from: {st.session_state.get('url', 'Unknown URL')}"
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the knowledge base..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            try:
                # Get agent response
                agent = st.session_state.agent
                response = agent.run(prompt)

                # Display response
                message_placeholder.markdown(response.get_content_as_string())

                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.get_content_as_string()}
                )

            except Exception as e:
                message_placeholder.error(f"Error getting response: {str(e)}")

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Instructions when no agent is loaded
else:
    st.divider()
    st.markdown(
        """
    ### 📋 How to use this playground:
    
    1. **Enter a URL** in the sidebar - this will be the website the agent learns from
    2. **Configure settings** like max links to crawl and model selection
    3. **Click "Initialize Agent"** to start the knowledge base loading process
    4. **Start chatting** with your agent about the website content!
    
    ### 🔧 Requirements:
    - MongoDB connection string in `.env` file (`mdb_url`)
    - Ollama running locally with the selected model
    - Internet connection to crawl the website
    """
    )

# Footer
st.divider()

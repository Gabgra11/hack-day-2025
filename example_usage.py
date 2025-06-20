"""
Example usage of the Agno Knowledge Base Playground
This script demonstrates how to use the playground programmatically
"""

from agno.agent import Agent
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.vectordb.mongodb import MongoDb
from agno.models.ollama import Ollama
from agno.embedder.ollama import OllamaEmbedder
import dotenv
import os

def create_agent_with_knowledge(url, model_id="llama3.1", max_links=10, collection_name="example_knowledge"):
    """
    Create an Agno agent with knowledge from a website
    
    Args:
        url (str): The website URL to crawl
        model_id (str): Ollama model to use
        max_links (int): Maximum number of links to crawl
        collection_name (str): MongoDB collection name
    
    Returns:
        Agent: Configured Agno agent
    """
    
    # Load environment variables
    dotenv.load_dotenv()
    
    # Initialize vector database
    vector_db = MongoDb(
        collection_name=collection_name,
        db_url=os.getenv("mdb_url"),
        embedder=OllamaEmbedder(id="openhermes")
    )
    
    # Create knowledge base
    knowledge_base = WebsiteKnowledgeBase(
        urls=[url], 
        max_links=max_links, 
        vector_db=vector_db
    )
    
    # Create agent
    agent = Agent(
        model=Ollama(id=model_id),
        knowledge=knowledge_base,
        markdown=True,
    )
    
    return agent

def main():
    """Example usage of the playground"""
    
    # Example 1: Create agent with Agno documentation
    print("🤖 Creating agent with Agno documentation...")
    agent = create_agent_with_knowledge(
        url="https://docs.agno.com/introduction",
        model_id="llama3.1",
        max_links=5,
        collection_name="agno_docs"
    )
    
    # Load knowledge base
    print("📚 Loading knowledge base...")
    agent.knowledge.load(recreate=True)
    
    # Ask questions
    questions = [
        "What is Agno?",
        "What are the main features of Agno?",
        "How do I create an agent with Agno?"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        response = agent.run(question)
        print(f"🤖 Answer: {response.get_content_as_string()}")
        print("-" * 50)

if __name__ == "__main__":
    main() 
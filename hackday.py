from agno.agent import Agent
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.vectordb.mongodb import MongoDb
from agno.models.ollama import Ollama
from agno.embedder.ollama import OllamaEmbedder
import dotenv
import os

dotenv.load_dotenv()

vector_db = MongoDb(
    collection_name="knowledge",
    db_url=os.getenv("mdb_url"),
    embedder=OllamaEmbedder(id="openhermes"),
)

knowledge_base = WebsiteKnowledgeBase(max_links=3, vector_db=vector_db)

agent = Agent(
    model=Ollama(id="llama3.1"),
    markdown=True,
    instructions="""
    You are an AI agent whose goal is to answer questions based on the provided knowledge base.
    You will be given a prompt, and you should use the knowledge base to provide an accurate and concise response.
    If the knowledge base does not contain relevant information, you should inform the user that you do not have enough information to answer their question.
    Always provide a response in markdown format.
    Always keep answers concise and to the point.
    """,
)


def load_knowledge_urls(urls):
    """
    Load knowledge URLs into the MongoDB vector database.

    Args:
        urls (list): List of URLs to load into the knowledge base.
    """
    try:
        knowledge_base.urls = urls
        knowledge_base.load(recreate=True)
        print(f"Loaded {len(urls)} URLs into the knowledge base.")
        return True
    except Exception as e:
        print(f"Error loading URLs: {e}")
        return False


def get_agent_response(prompt):
    """
    Get a response from the agent based on the provided prompt.

    Args:
        prompt (str): The prompt to send to the agent.

    Returns:
        str: The response from the agent.
    """
    try:
        agent.knowledge = knowledge_base
        runResponse = agent.run(prompt)
        return runResponse.content
    except Exception as e:
        print(f"Error getting agent response: {e}")
        return None

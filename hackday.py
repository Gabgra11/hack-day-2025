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

knowledge_base = WebsiteKnowledgeBase(
    urls=["https://docs.agno.com/introduction"],
    max_links=10,
    vector_db=vector_db
)

knowledge_base.load(recreate=False)

agent = Agent(
    model=Ollama(id="llama3.1"),
    knowledge=knowledge_base,
    markdown=True,
)

agent.print_response("Summarize the contents of the knowledge base in a single paragraph.")
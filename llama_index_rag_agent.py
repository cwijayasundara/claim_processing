import warnings
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import (
    FunctionCallingAgentWorker,
)

warnings.filterwarnings('ignore')
_ = load_dotenv()

llm = OpenAI(model="gpt-4o-mini", temperature=0.1)

embed_model = OpenAIEmbedding(model="text-embedding-3-small")

Settings.llm = llm
Settings.embed_model = embed_model

def search_policy_document(document_path:str, query: str) -> str:
    """Search the policy document for the given query and returns the response"""

    insurance_policy_docs = (SimpleDirectoryReader (input_files=[document_path]).load_data())
    insurance_index = VectorStoreIndex.from_documents(insurance_policy_docs)
    insurance_query_engine = insurance_index.as_query_engine(similarity_top_k=3)

    query_engine_tools = [
        QueryEngineTool(
            query_engine=insurance_query_engine,
            metadata=ToolMetadata(
                name="insurance_policy_document",
                description="Provides information about insurance and claim policies",
            ),
        )
    ]

    agent_worker = FunctionCallingAgentWorker.from_tools(
        query_engine_tools,
        llm=llm,
        verbose=True,
        allow_parallel_tool_calls=False,
    )

    agent = agent_worker.as_agent()

    response = agent.chat(query)
    return response.response

# # Test the search_policy_document function
# policy_document_path = "docs/policy/pb116349-business-health-select-handbook-1024-pdfa.pdf"
# response_1 = search_policy_document(policy_document_path, "Whats the cashback option for dental fees?")
# print("RAG response 1:", response_1)
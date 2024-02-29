#I want to parse my documents into smaller chunks”

# Local settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Global settings
from llama_index.core import Settings
Settings.chunk_size = 512

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(
    documents, transformations=[SentenceSplitter(chunk_size=512)]
)

query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)
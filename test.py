# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.llms.ollama import Ollama

# documents = SimpleDirectoryReader("data").load_data()

# # bge-base embedding model
# Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")# unsloth/Llama-3.2-3B-Instruct")#BAAI/bge-base-en-v1.5")

# # ollama
# Settings.llm = Ollama(model="llama3.2:latest", request_timeout=360.0)

# index = VectorStoreIndex.from_documents(
#     documents,
# )

# query_engine = index.as_query_engine()
# response = query_engine.query("What did the author do growing up?")
# print(response)

from pathlib import Path
from llama_index.core import (
    VectorStoreIndex,
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama


def main():
    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")
    Settings.llm = Ollama(model="hf.co/wanshenl/pgsql-performance:latest", request_timeout=360.0)

    PERSIST_DIR = Path("storage")
    if not PERSIST_DIR.exists():
        commits = SimpleDirectoryReader("commits").load_data(num_workers=40)
        mailinglists = SimpleDirectoryReader("mailinglists").load_data(num_workers=40)
        index = VectorStoreIndex.from_documents(commits + mailinglists, show_progress=True)
        index.storage_context.persist(persist_dir=PERSIST_DIR)

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()
    response = query_engine.query("What kind of information is available?")
    print(response)


if __name__ == "__main__":
    main()

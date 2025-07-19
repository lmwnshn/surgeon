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
    Settings.embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            #model_name="BAAI/bge-small-en-v1.5",
            #model_name="sentence-transformers/all-mpnet-base-v2",
    )
    Settings.llm = Ollama(
            #model="hf.co/wanshenl/pgsql-performance:latest",
            model="llama3.2:latest",
            request_timeout=360.0,
            temperature=0,
    )

    PERSIST_DIR = Path("storage")
    if not PERSIST_DIR.exists():
        #commits = SimpleDirectoryReader("commits").load_data(num_workers=40)
        mailinglists = SimpleDirectoryReader("mailinglists/meow").load_data(num_workers=40)
        index = VectorStoreIndex.from_documents(mailinglists, show_progress=True)
        index.storage_context.persist(persist_dir=PERSIST_DIR)

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

#    retriever = VectorIndexRetriever(
#        index=index,
#        similarity_top_k=10,
#    )
#
#    response_synthesizer = get_response_synthesizer()
#
#    query_engine = RetrieverQueryEngine(
#        retriever=retriever,
#        response_synthesizer=response_synthesizer,
#        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
#    )

    query_engine = index.as_query_engine()#similarity_top_k=10)
    #response = query_engine.query("""Highlight performance regressions when upgrading from PostgreSQL version 15 to version 16, justify each complaint with short and concise snippets from the mailing list.""")
    #response = query_engine.query("""Highlight the characteristics of SQL queries that experience performance regressions in PostgreSQL v16. Only include characteristics that are definitely a problem, you must justify each complaint with concise links to mailing list threads.""")
    #response = query_engine.query("""Will the following SQL query experience regressions in PostgreSQL? Reply Yes, No, or Maybe. If you reply Yes or No, you must provide justification by quoting from the mailing list. SQL: SELECT DISTINCT foo from bar;""")
    #response = query_engine.query("""Using information from the mailing list, will the SQL query "SELECT DISTINCT foo from bar" experience regressions in PostgreSQL? Let's think step by step.""")
    #response = query_engine.query("""Using information from the mailing list, will the SQL query "SELECT DISTINCT foo from bar, unnest(string_to_array('woof,meow',','))" experience regressions in PostgreSQL? Let's think step by step.""")
    #response = query_engine.query("""Let's think step by step. Using information from the mailing list, are there performance regressions for the SQL query "SELECT DISTINCT foo from bar, unnest(string_to_array('woof,meow',','))"?""")
    response = query_engine.query("""Let's think step by step. With reference to snippets from the mailing list, are there performance regressions that are newly introduced by Postgres 16?""")
#"""
#You are an expert PostgreSQL developer helping people on the 'pgsql-performance' mailing list.
#You are composing a reply to resolve the email chain below.
#
#### Original Email:
#Date: 2024-11-13
#Subject: Performance regressions when upgrading from v15 to v16
#Contents: What SQL queries are known to have regressions when upgrading from v15 to v16?
#
#### Some emails may be omitted for brevity.
#
#### Latest Email:
#Date: 2024-11-13
#Subject: Performance regressions when upgrading from v15 to v16
#Contents: What SQL queries are known to have regressions when upgrading from v15 to v16?
#
#### Your Response:
#""")
    print(response)


if __name__ == "__main__":
    main()

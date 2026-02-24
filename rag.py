import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def retrieve_planning_context(jira_description, k=6):
    """
    Retrieve context based on Jira requirements.
    Used for implementation planning.
    """
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

    vectorstore = FAISS.load_local(
        "repo_index",
        embeddings,
        allow_dangerous_deserialization=True
    )


    docs = vectorstore.similarity_search(jira_description, k=k)

    return "\n\n".join(doc.page_content for doc in docs)

def retrieve_context(diff, changed_files):

    if not os.path.exists("repo_index"):
        return "Repository index not found."

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

    vectorstore = FAISS.load_local(
        "repo_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retrieved_docs = []

    # 🔹 Retrieve by file name first
    for file_name in changed_files:
        file_hits = vectorstore.similarity_search(file_name, k=3)
        retrieved_docs.extend(file_hits)

    # 🔹 Semantic retrieval using diff
    semantic_hits = vectorstore.similarity_search(diff, k=7)
    retrieved_docs.extend(semantic_hits)

    # Remove duplicates
    unique_docs = {doc.page_content: doc for doc in retrieved_docs}.values()

    print("Total retrieved chunks:", len(unique_docs))

    if not unique_docs:
        return "No relevant repository context found."

    return "\n\n".join(doc.page_content for doc in unique_docs)
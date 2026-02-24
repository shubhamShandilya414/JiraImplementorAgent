import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document



def index_repo(repo_path):
    documents = []
    print("Files being indexed:")
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".java", ".py", ".js")):
                full_path = os.path.join(root, file)
                print(full_path)

                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    documents.append(
                        Document(
                            page_content=content,
                            metadata={"file_path": full_path}
                        )
                    )

    print("Total files indexed:", len(documents))


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(documents)

    print("Total chunks created:", len(split_docs))

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

    vectorstore = FAISS.from_documents(split_docs, embeddings)

    vectorstore.save_local("repo_index")

    print("FAISS index created successfully.")


if __name__ == "__main__":
    index_repo("/Users/shubhamshandilya/Downloads/order-service-master")
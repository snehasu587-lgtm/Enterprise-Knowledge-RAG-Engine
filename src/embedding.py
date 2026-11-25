from sentence_transformers import SentenceTransformer
from src.text_splitter import split_documents
from src.document_loader import load_pdf


def create_embeddings(chunks):

    print("\nLoading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [chunk.page_content for chunk in chunks]

    embeddings = model.encode(texts)

    print("\nEmbeddings created successfully!")
    print("Total embeddings:", len(embeddings))
    print("Embedding dimensions:", embeddings.shape)

    return embeddings


if __name__ == "__main__":
    documents = load_pdf("documents/sample.pdf")

    chunks = split_documents(documents)

    embeddings = create_embeddings(chunks)

    from vector_store import create_vector_store

    create_vector_store(chunks, embeddings)


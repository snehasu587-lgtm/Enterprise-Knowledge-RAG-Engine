import chromadb
import uuid


def create_vector_store(chunks, embeddings):

    print("\nCreating vector database...")

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        name="enterprise_knowledge"
    )

    if not chunks:
        raise ValueError("No document chunks to store.")

    filename = chunks[0].metadata["file_name"]

    # Remove previous chunks of this same PDF
    existing = collection.get(
        where={"file_name": filename}
    )

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    # Store new chunks
    collection.add(
        ids=[str(uuid.uuid4()) for _ in chunks],
        documents=[
            chunk.page_content for chunk in chunks
        ],
        embeddings=embeddings.tolist(),
        metadatas=[
            chunk.metadata for chunk in chunks
        ]
    )

    print("Vector database updated successfully!")
    print("Total stored documents:", collection.count())
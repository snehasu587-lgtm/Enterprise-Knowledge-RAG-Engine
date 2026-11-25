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

    print("\nVector database updated successfully!")
    print("Total stored documents:", collection.count())

    return collection
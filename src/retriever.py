import chromadb
from sentence_transformers import SentenceTransformer


def retrieve_documents(query, file_name, top_k=3):

    print("\nSearching relevant documents...")

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Connect to ChromaDB
    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_collection(
        name="enterprise_knowledge"
    )

    # Convert question into embedding
    query_embedding = model.encode(
        [query]
    ).tolist()

    # Retrieve relevant chunks from the selected PDF
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where={"file_name": file_name},
        include=["documents", "metadatas", "distances"]
    )

    # Remove exact duplicate text chunks
    unique_results = {
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]]
    }

    seen = set()

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        cleaned_text = document.strip()

        if cleaned_text and cleaned_text not in seen:

            seen.add(cleaned_text)

            unique_results["documents"][0].append(document)
            unique_results["metadatas"][0].append(metadata)
            unique_results["distances"][0].append(distance)

    print("Retrieved unique chunks:", len(unique_results["documents"][0]))

    return unique_results
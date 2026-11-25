from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.document_loader import load_pdf

def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---")
        print(chunk.page_content)

    return chunks


if __name__ == "__main__":

    pdf_path = "documents/sample.pdf"

    documents = load_pdf(pdf_path)

    chunks = split_documents(documents)
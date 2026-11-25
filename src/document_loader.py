from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path, original_filename=None):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    loader = PyPDFLoader(str(path))
    documents = loader.load()

    filename = original_filename or path.name

    for doc in documents:
        doc.metadata["file_name"] = filename

    print(f"Successfully loaded: {filename}")
    print(f"Total pages: {len(documents)}")

    return documents
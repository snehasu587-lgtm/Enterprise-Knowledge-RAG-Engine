# Enterprise Knowledge RAG Engine

An AI-powered document question-answering system built using Retrieval-Augmented Generation (RAG). It allows users to upload PDF documents and ask questions based on their content.

## Features

- Upload and process PDF documents
- Extract text from PDF files
- Split documents into smaller chunks
- Generate dense embeddings using Sentence Transformers
- Store embeddings in ChromaDB
- Retrieve relevant document chunks using semantic similarity
- Generate answers using Google Gemini
- Display source citations with PDF filename and page number
- Remove duplicate retrieved chunks
- Reduce hallucinations by grounding answers in retrieved context

## Technologies Used

- Python
- Streamlit
- LangChain Community
- Sentence Transformers
- ChromaDB
- Google Gemini API
- PyPDF

## Project Structure

```text
Enterprise-Knowledge-RAG-Engine/
│
├── documents/
├── src/
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── embedding.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── llm.py
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/snehasu587-lgtm/Enterprise-Knowledge-RAG-Engine.git
```

2. Open the project folder:

```bash
cd Enterprise-Knowledge-RAG-Engine
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate it on Windows:

```powershell
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

## API Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never upload your actual API key to GitHub.

## Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## How It Works

1. User uploads a PDF document.
2. The system extracts text from the PDF.
3. Extracted text is divided into smaller chunks.
4. Sentence Transformers generates embeddings.
5. ChromaDB stores the document chunks and embeddings.
6. The user's question is converted into an embedding.
7. Relevant chunks are retrieved using semantic similarity.
8. Gemini generates an answer using the retrieved context.
9. The application displays the answer and source citations.

## Testing

The application was tested with PDF documents using questions about document content.

Test cases include:

- Asking questions about certifications.
- Retrieving information from uploaded resumes.
- Checking source filename and page number citations.
- Asking questions about information not present in the document to test hallucination control.
- Checking duplicate chunk removal.

## Author

Developed as an internship project.

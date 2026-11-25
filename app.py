import streamlit as st
import tempfile
import os

from src.document_loader import load_pdf
from src.text_splitter import split_documents
from src.embedding import create_embeddings
from src.vector_store import create_vector_store
from src.retriever import retrieve_documents
from src.llm import generate_answer


st.set_page_config(
    page_title="Enterprise Knowledge RAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Enterprise Knowledge RAG Engine")
st.write("Upload your PDF and ask questions using AI.")

uploaded_file = st.file_uploader(
    "Upload your PDF document",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Process PDF"):

        with st.spinner("Processing your document..."):

            temp_path = None

            try:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(uploaded_file.getvalue())
                    temp_path = temp_file.name

                documents = load_pdf(
                    temp_path,
                    original_filename=uploaded_file.name
                )

                chunks = split_documents(documents)

                embeddings = create_embeddings(chunks)

                create_vector_store(chunks, embeddings)

                st.session_state["active_pdf"] = uploaded_file.name

                st.success("PDF processed successfully!")

            except Exception as e:
                st.error(f"Processing error: {e}")

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)


st.subheader("Ask Questions")

active_pdf = st.session_state.get("active_pdf")

if uploaded_file is not None:

    if active_pdf != uploaded_file.name:
        st.warning(
            "New PDF selected. Please click Process PDF before asking questions."
        )
        active_pdf = None
if active_pdf:
    st.info(f"Currently selected document: {active_pdf}")

    question = st.text_input("Enter your question:")

    if st.button("Generate Answer"):

        if question.strip():

            with st.spinner("Searching for answers..."):

                try:
                    results = retrieve_documents(
                        question,
                        file_name=active_pdf
                    )

                    documents = results.get(
                        "documents", [[]]
                    )[0]

                    if not documents:
                        st.warning(
                            "No relevant information found in this PDF."
                        )

                    else:
                        context = "\n".join(documents)

                        st.subheader("Retrieved Document Context")
                        st.write(context)

                        answer = generate_answer(
                        context,
                        question
                        )

                        st.subheader("AI Generated Answer")
                        st.write(answer)

                        st.subheader("Source Citations")

                        metadatas = results.get("metadatas", [[]])[0]

                        for metadata in metadatas:
                            file_name = metadata.get("file_name", "Unknown file")
                            page_number = metadata.get("page", "Unknown")

                            if isinstance(page_number, int):
                                page_number += 1
                            st.write(
                                f"Source: {file_name} | Page: {page_number}"
                            )

                except Exception as e:
                    st.error(f"Error: {e}")

        else:
            st.warning("Please enter a question.")

else:
    st.info("Please upload and process a PDF first.")
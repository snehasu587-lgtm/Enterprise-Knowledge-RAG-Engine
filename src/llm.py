import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def generate_answer(context, question):

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Answer the user's question using ONLY the information
provided in the context below.

Rules:
1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the answer is not available in the context, say:
   "The uploaded document does not contain enough information
   to answer this question."
4. Give clear, accurate and concise answers.
5. Use bullet points when listing multiple items.

Context:
{context}

Question:
{question}

Answer:
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            if response.text:
                return response.text

            return "No answer was generated. Please try again."

        except Exception as e:
            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue

                return (
                    "Gemini is currently experiencing high demand. "
                    "Please try again after a few moments."
                )

            raise e


if __name__ == "__main__":
    answer = generate_answer(
        "RAG stands for Retrieval Augmented Generation.",
        "What is RAG?"
    )

    print(answer)
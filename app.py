
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Load and embed documents
def setup_vectorstore():
    loader = TextLoader("knowledge_base/faq.txt")
    documents = loader.load()
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents, embeddings, persist_directory="embeddings")
    vectordb.persist()
    return vectordb

vectordb = setup_vectorstore()

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json["question"]
    docs = vectordb.similarity_search(user_question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""
You are a helpful customer support agent. Use the context below to answer the customer question:

Context:
{context}

Question: {user_question}
Answer:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3
    )
    answer = response["choices"][0]["message"]["content"].strip()
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True)

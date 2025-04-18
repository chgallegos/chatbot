from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import uuid
from werkzeug.utils import secure_filename
from langchain_community.document_loaders import TextLoader, UnstructuredPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["POST", "OPTIONS"])

UPLOAD_FOLDER = "user_data"
ALLOWED_EXTENSIONS = {"pdf", "txt"}

user_stores = {}  # in-memory cache

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_path(user_id):
    return os.path.join(UPLOAD_FOLDER, user_id)

def get_vectorstore(user_id):
    if user_id in user_stores:
        return user_stores[user_id]

    vectordb_path = os.path.join(get_user_path(user_id), "chroma")
    if not os.path.exists(vectordb_path):
        return None
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=vectordb_path, embedding_function=embeddings)
    user_stores[user_id] = vectordb
    return vectordb

def build_vectorstore(user_id):
    user_path = get_user_path(user_id)
    files_path = os.path.join(user_path, "files")
    vectordb_path = os.path.join(user_path, "chroma")

    documents = []
    embeddings = OpenAIEmbeddings()

    for filename in os.listdir(files_path):
        filepath = os.path.join(files_path, filename)
        if filename.endswith(".txt"):
            loader = TextLoader(filepath)
        elif filename.endswith(".pdf"):
            loader = UnstructuredPDFLoader(filepath)
        else:
            continue
        documents.extend(loader.load())

    vectordb = Chroma.from_documents(documents, embeddings, persist_directory=vectordb_path)
    user_stores[user_id] = vectordb  # update cache
    return vectordb

@app.route("/upload", methods=["POST"])
def upload():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400

    user_path = get_user_path(user_id)
    files_path = os.path.join(user_path, "files")
    os.makedirs(files_path, exist_ok=True)

    uploaded_files = request.files.getlist("files")
    if not uploaded_files:
        return jsonify({"error": "No files selected"}), 400

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(files_path, filename))

    vectordb = build_vectorstore(user_id)
    return jsonify({"message": "Files uploaded and indexed."})

@app.route("/ask", methods=["POST"])
def ask():
    user_id = request.json.get("user_id")
    user_question = request.json.get("question", "")

    vectordb = get_vectorstore(user_id)
    if not vectordb:
        return jsonify({"error": "No knowledge base found. Please upload a file first."}), 404

    docs = vectordb.similarity_search(user_question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a helpful customer support agent. Use the context below to answer the customer question:

Context:
{context}

Question: {user_question}
Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3
    )

    answer = response.choices[0].message.content.strip()
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True)

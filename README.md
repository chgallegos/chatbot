# 🧠 Chatbot – AI-Powered Document QA Assistant

This project is a lightweight, GPT-powered chatbot that allows users to upload documents and ask natural language questions. It retrieves relevant information from multiple files and provides context-aware answers — ideal for internal knowledge bases, customer support, or personal research.

## 🚀 Features

- 📄 Upload multiple file types (PDF, DOCX, TXT, etc.)
- 🔍 Semantic search using vector embeddings
- 🤖 Answers powered by OpenAI’s GPT-4 API
- 🧠 Memory-aware follow-up conversations
- 🔒 Per-user file handling (designed for future authentication support)
- 🛠️ Clean Flask backend and modular architecture

## 🖼️ Demo Screenshot

![Chatbot UI](/Resources/demo-screenshot.png)

## 🧪 Example Use Case

Upload your company’s product manual, refund policy, and support playbook — then ask:
> “How do I request a refund and how long does it take?”

The chatbot will pull information from multiple files and respond intelligently.

## 🧱 Tech Stack

- **Backend:** Python, Flask
- **AI Model:** OpenAI GPT-4 via `openai` API
- **Vector Store:** In-memory (easily swappable for FAISS, Qdrant, Pinecone, etc.)
- **Frontend:** HTML, JavaScript, CSS (can be replaced with React or any framework)

## 🛠️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/chgallegos/chatbot.git
cd chatbot
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file and add your OpenAI key:

```env
OPENAI_API_KEY=your-openai-api-key
```

4. **Run the app**

```bash
python app.py
```

5. **Go to:**  
[http://localhost:5000](http://localhost:5000)

## 📁 Project Structure

```
chatbot/
├── app.py               # Flask app
├── routes.py            # Upload and chat endpoints
├── vector_store.py      # Embedding & retrieval logic
├── templates/           # HTML files
├── static/              # CSS and JS
├── utils/               # Text extraction and chunking
├── requirements.txt     
└── .env.example         
```

## ⚠️ Deployment Note

This app is hosted on [Render.com](https://render.com), which spins down after periods of inactivity. Each time it restarts, a manual redeploy is currently required for proper functionality. For persistent uptime, consider hosting on a platform with cold-start support or container persistence.

## 📚 Future Improvements

- Firebase authentication (WIP)
- Persistent vector storage per user
- Admin dashboard for document and chat tracking
- Upload UI with drag-and-drop + progress indicators
- Dark mode + responsive UI

## 🤝 License

MIT License. Use freely, but attribution is appreciated.

## ✨ Author

Built by [Christopher Gallegos](https://github.com/chgallegos)

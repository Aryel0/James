# James – AI Game Chat Assistant 

**James** is a lightweight desktop chat assistant built with Python and PyQt5 that answers video game-related questions using local AI. Under the hood, James combines **LLaMA 3.2** via **Ollama**, **LangChain**, and **ChromaDB** to provide fast and context-aware responses using **Retrieval-Augmented Generation (RAG)**.

---

## Features

- AI answers powered by **LLaMA 3.2 (via Ollama)** and **LangChain**
- Integrated **RAG pipeline** with vector embeddings stored in **ChromaDB**
- Chat-style interface with readable user and AI message formatting
- Multiple built-in themes (Dark, Green, Grey, Light, Pink)
- Built entirely in Python using **PyQt5** (no web browser needed)
- Modular design for easily swapping models, prompts, or database

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/james-chat-assistant.git
cd james-chat-assistant

### 2. Install Dependencies
pip install -r requirements.txt

### 3.Make sure ollama is running and llama3.2 is pulled
```bash
ollama run --model /path/to/llama3.2

### 4. Run the Application
python main.py
```

## How it Works
James integrates:

Ollama to run the LLaMA 3.2 model locally

LangChain to manage AI interactions, prompt routing, and tool usage

ChromaDB as a vector store for documents, enabling RAG to inject relevant knowledge into each AI response

Together, these allow James to answer your game-related queries intelligently with up-to-date, searchable context.

## Structure

The application is structured as follows:
.
├── main.py               # PyQt5 GUI
├── jamesllm.py           # LangChain / Ollama 
├── vector.py             # ChromaDB / RAG logic
├── ressources/
│   ├── james_icon.png
│   ├── dark.qss
│   ├── grey.qss
│   └── green.qss
|____chromadb/             # ChromaDB vector store


author: Aryel-[https://github.com/Aryel0]

# 📊 StatBot Pro: Full-Stack AI Data Analyst

StatBot Pro is an autonomous Agentic AI application that acts as a virtual data analyst. Users can upload raw CSV datasets and ask complex business questions in natural language. Under the hood, the AI autonomously writes Pandas/Python code, executes it, and dynamically generates custom Matplotlib visualizations—all served to a modern React frontend.

## ✨ Key Features
* **Autonomous Code Execution:** The AI translates natural language into executable Python logic to filter and analyze data.
* **Dynamic Visualizations:** Automatically generates and serves high-res charts via a REST API.
* **Modern Architecture:** Built with a decoupled FastAPI backend and a Next.js (React) frontend.
* **Premium UI/UX:** Sleek dark-mode interface with real-time chat and file uploading.

## 🛠️ Tech Stack
* **Frontend:** Next.js, Tailwind CSS
* **Backend:** FastAPI, Uvicorn, LangChain
* **AI:** Google Gemini 2.5 Flash Lite
* **Data:** Pandas, Matplotlib

## 🚀 Quick Start Guide

### 1️⃣ Start the AI Backend (FastAPI)
```bash
.\.venv\Scripts\python.exe -m uvicorn api:app
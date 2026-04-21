from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import os
import io
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

app = FastAPI(title="StatBot Pro Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Tell FastAPI to serve files from the current folder so React can see them
app.mount("/static", StaticFiles(directory="."), name="static")

os.environ["GOOGLE_API_KEY"] = "API"
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-lite", temperature=0)
current_df = None
agent_executor = None
class ChatRequest(BaseModel):
    message: str
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global current_df, agent_executor
    try:
        contents = await file.read()
        current_df = pd.read_csv(io.BytesIO(contents))
        agent_executor = create_pandas_dataframe_agent(llm, current_df, verbose=True, allow_dangerous_code=True)
        return {"status": "success", "message": f"Loaded {file.filename} ({len(current_df)} rows)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
@app.post("/chat")
async def chat_with_bot(request: ChatRequest):
    global agent_executor
    if agent_executor is None:
        return {"status": "error", "message": "Please upload a CSV file in the sidebar first!"}
        
    #Generate a unique name for the chart and strict graphing rules
    unique_name = f"chart_{int(time.time())}.png"
    full_prompt = f"""
    Question: {request.message}
    Rules: If you make a chart, save it exactly as '{unique_name}' in the current directory. 
    Do NOT use plt.show(). Always use plt.tight_layout() before saving.
    """

    try:
        response = agent_executor.invoke({"input": full_prompt})
        
        # Check if the AI actually created a chart
        image_url = None
        if os.path.exists(unique_name):
            image_url = f"http://127.0.0.1:8000/static/{unique_name}"
        return {
            "status": "success",
            "bot_answer": response['output'],
            "image_url": image_url  # Send the URL back to React!
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
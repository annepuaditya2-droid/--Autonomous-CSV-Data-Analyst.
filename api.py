import os
import io
import time
import pandas as pd
import uvicorn
import matplotlib.pyplot as plt
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# LangChain & Google AI Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv

load_dotenv()

# 1. Setup Directories
if not os.path.exists("static"):
    os.makedirs("static")

app = FastAPI()

# 2. CORS Setup (Next.js communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Static Files Mounting (Serves the charts to the web browser)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. AI Setup
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
current_df = None
agent_executor = None

class ChatRequest(BaseModel):
    message: str

# 5. Upload Route
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global current_df, agent_executor
    try:
        contents = await file.read()
        current_df = pd.read_csv(io.StringIO(contents.decode('utf-8'))) 
        
        # We give the AI a clear "Persona" and strict rules for charts
        prefix = """
        You are a data visualizer.
        When asked for a chart, graph, or picture:
        1. Use matplotlib to create it.
        2. Save it to 'static/chart.png' using plt.savefig('static/chart.png').
        3. ALWAYS call plt.close() after saving.
        4. Final Answer: 'I have generated the chart for you.'
        5. Just run the code, do not explain it unless asked.
        """

        agent_executor = create_pandas_dataframe_agent(
            llm,
            current_df,
            verbose=True,
            allow_dangerous_code=True,
            prefix=prefix,
            handle_parsing_errors=True # This allows the agent to recover from formatting issues
        )
        return {"status": "success", "message": "Data loaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Chat Route (The "Bulletproof" Version)
@app.post("/chat")
async def chat_with_data(request: ChatRequest):
    global agent_executor
    
    if agent_executor is None:
        return {"response": "Please upload a CSV file first."}
        
    final_response = ""
    try:
        # Clear old chart before starting new task
        if os.path.exists("static/chart.png"):
            os.remove("static/chart.png")

        # Run the agent
        # We use .invoke instead of .run for better stability in newer LangChain versions
        result = agent_executor.invoke({"input": request.message})
        final_response = result.get("output", "I processed your request but couldn't generate a text response.")
        
    except Exception as e:
        # RECOVERY LOGIC: If LangChain fails to "parse", the AI usually DID the work
        # but the agent got confused by the wording. We grab the text anyway.
        error_msg = str(e)
        if "Could not parse LLM output: `" in error_msg:
            # Extract the actual answer from the error message
            final_response = error_msg.split("Could not parse LLM output: `")[1].rstrip("`")
        else:
            final_response = f"I encountered an issue, but I'll try to check for data: {error_msg}"

    # 7. Check for Image (The "Pop-up" Logic)
    image_url = None
    if os.path.exists("static/chart.png"):
        # Add a timestamp so the browser doesn't cache the old image
        timestamp = int(time.time())
        image_url = f"http://127.0.0.1:8000/static/chart.png?t={timestamp}"

    return {
        "response": final_response, 
        "image_url": image_url
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import generate_evaluation
from models import IlanMetni
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/evaluate")
async def evaluate(data: IlanMetni):
    print("Gelen metin:", data.metin)  # Debug için
    result = await generate_evaluation(data.dict())
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

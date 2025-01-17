from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict
from uuid import uuid4
import httpx
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, VideoUnavailable

app = FastAPI()

# In-memory storage for job status
jobs: Dict[str, Dict] = {}

class TranscriptionRequest(BaseModel):
    urls: List[str]
    callback_url: str

class CallbackRequest(BaseModel):
    url: str
    transcript: str

@app.post("/transcribe")
def transcribe(request: TranscriptionRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid4())
    jobs[job_id] = {"status": "in_progress", "callback_url": request.callback_url, "results": []}
    
    background_tasks.add_task(process_transcription, job_id, request.urls, request.callback_url)
    
    return {"job_id": job_id, "status": "in_progress"}

async def process_transcription(job_id: str, urls: List[str], callback_url: str):
    results = []
    
    for url in urls:
        try:
            video_id = extract_video_id(url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([entry['text'] for entry in transcript])
            results.append({"url": url, "transcript": transcript_text})
        except (NoTranscriptFound, VideoUnavailable):
            results.append({"url": url, "error": "Transcript not available or video unavailable."})
        except Exception as e:
            results.append({"url": url, "error": str(e)})

    jobs[job_id]["status"] = "completed"
    jobs[job_id]["results"] = results

    # Send results to callback URL
    async with httpx.AsyncClient() as client:
        try:
            await client.post(callback_url, json={"job_id": job_id, "results": results})
        except Exception as e:
            jobs[job_id]["callback_error"] = str(e)

@app.post("/transcribe/callback/{job_id}")
def callback(job_id: str, request: CallbackRequest):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job ID not found")

    return {"message": "Callback received", "job_id": job_id, "url": request.url, "transcript": request.transcript}

def extract_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    else:
        raise ValueError("Invalid YouTube URL")

@app.get("/job/{job_id}")
def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job ID not found")

    return jobs[job_id]

# Run this API with Uvicorn or another ASGI server
# Example: uvicorn main:app --reload

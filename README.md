
# YouTube Transcription API

The YouTube Transcription API is a Python-based solution for transcribing YouTube videos into text. It uses the FastAPI framework for building APIs and the youtube-transcript-api library to fetch transcripts. The API supports asynchronous processing with a Request-Reply pattern and a callback mechanism.




## Features

- Transcription Job Submission:  
    Accepts a list of YouTube URLs and a callback URL.  
    Returns a job_id immediately for tracking.

- Asynchronous Processing:    
    Long-running transcription tasks are handled in the background.
    Results are sent to the provided callback URL.

- Job Status Retrieval:  
    Allows users to check the status of their transcription jobs.

- Error Handling:     
    Gracefully handles unavailable transcripts or invalid YouTube URLs.


## Endpoints

  1. POST /transcribe  
 
   Request body :


```python
{
  "urls": ["<YouTube_URL_1>", "<YouTube_URL_2>"],
  "callback_url": "<Callback_URL>"
}
```

Response :

```python
{
  "job_id": "<unique_job_id>",
  "status": "in_progress"
}
```

2. POST /transcribe/callback/{job_id}
 
   Request body :


```python
{
  "url": "<YouTube_URL>",
  "transcript": "<Transcript_Text>"
}
```

Response :

```python
{
  "message": "Callback received",
  "job_id": "<unique_job_id>",
  "url": "<YouTube_URL>",
  "transcript": "<Transcript_Text>"
}
```

3. GET /job/{job_id}
 
 
Response :

```python
{
  "status": "completed",
  "callback_url": "<Callback_URL>",
  "results": [
    {
      "url": "<YouTube_URL>",
      "transcript": "<Transcript_Text>"
    },
    {
      "url": "<YouTube_URL>",
      "error": "<Error_Message>"
    }
  ]
}
```



## Installation



1. Clone the repository:    

 


```bash
  git clone https://github.com/<your-username>/youtube-transcription-api.git 
  cd youtube-transcription-api
```


2. Clone the repository:   

        

```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:  
  

 



```bash
  pip install -r requirements.txt
```

4. Run the server:  
  


 
```bash
  uvicorn main:app --reload
```

5. Access the API documentation at: ```http://127.0.0.1:8000/docs```
## Deployment

To deploy the application:

Use a cloud service (e.g., AWS, Azure, GCP) or containerize it with Docker.

Add production-ready settings (e.g., Gunicorn for WSGI, HTTPS).

## Contributing

1. Fork the repository.

2. Create a new branch:

  ```
  git checkout -b feature-branch
  ```

3. Commit changes and push:

 
  ```
  git commit -m "Add new feature"
  git push origin feature-branch
  ```

4. Open a pull request.
## Acknowledgements

 - FastAPI

- YouTube Transcript API
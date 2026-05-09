from fastapi import FastAPI,Query
from client.rq_client import queue
from queues.workers import process_query

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat")
def  chat(query:str = Query(..., description="The query to chat with the model")):
    job = queue.enqueue(process_query, query)  # Process the query and generate a response
    return {"status": "queued", "job_id": job.id}

@app.get('/job-status')
def get_result(job_id:str = Query(..., description="The ID of the job to retrieve the result for")):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    
    return { "result":  result}
  

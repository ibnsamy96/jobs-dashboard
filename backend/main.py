from fastapi import FastAPI
from fastapi.param_functions import Query

import wuzzuf_jobs as wuzzufJ
import workable_jobs as workableJ


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome home, son!"}


@app.get("/all-jobs")
def fetchAll(query: str):
    all_jobs = []
    jobs_count = 0
    wuzzuf_jobs = fetchWuzzuf(query)
    all_jobs.append(wuzzuf_jobs)
    jobs_count += wuzzuf_jobs["count"]
    workable_jobs = fetchWorkable(query)
    all_jobs.append(workable_jobs)
    jobs_count += workable_jobs["count"]
    return {"total-count": jobs_count, "results": all_jobs}


@app.get("/wuzzuf")
def fetchWuzzuf(query: str):
    wuzzuf_jobs = wuzzufJ.getJobs(query)
    return wuzzuf_jobs


@app.get("/workable")
def fetchWorkable(query: str):
    workable_jobs = workableJ.getJobs(query)
    return workable_jobs


@app.get("/telegram/login")
def fetchWorkable(query: str, phone: str):
    workable_jobs = workableJ.getJobs(query)
    return workable_jobs


@app.get("/telegram")
def fetchWorkable(query: str, phone: str):
    workable_jobs = workableJ.getJobs(query)
    return workable_jobs


# wuzzuf_jobs = wuzzufJ.getJobs("front end development")
# workable_jobs = workableJ.getJobs("front end development")

# print(wuzzuf_jobs)
# print(workable_jobs)

import requests as rq
from bs4 import BeautifulSoup


def getStringFromHTML(html_code):
    soup = BeautifulSoup(html_code, "html.parser")
    return soup.text


def extractJobDescriptionText(job: dict):
    if "description" in job.keys():
        job["description"] = getStringFromHTML(job["description"])
    if "company" in job.keys() and "description" in job["company"].keys():
        job["company"]["description"] = getStringFromHTML(job["company"]["description"])
    return job


def generateSearchPageLink(query: str, offset: int):
    query_link = f"https://job-board.workable.com/api/v1/jobs?query={query}&location=Egypt&orderBy=postingUpdateTime+desc&remote=false&offset={offset}"
    return query_link


def findIsLastPage(fetchedData):
    if "nextPageToken" not in fetchedData.keys():
        return True
    return False


def fetchJobs(query: str, offset: int):
    request = rq.get(generateSearchPageLink(query=query, offset=offset))
    json = request.json()
    return json


def getAndConcatenateData(query: str):
    all_jobs = []
    jobs_count = 0

    offset = 0
    maximum_offset = 100  # maximum number of retrieved jobs

    while offset < maximum_offset:
        fetchedData = fetchJobs(query=query, offset=offset)
        page_jobs = fetchedData["jobs"]
        page_jobs = map(extractJobDescriptionText, page_jobs)
        all_jobs.extend(page_jobs)

        isLastPage: bool = findIsLastPage(fetchedData)
        if isLastPage:
            jobs_count = int(fetchedData["totalSize"])
            break
        offset += 10

    return jobs_count, all_jobs


def getJobs(query: str):
    jobs_count, all_jobs = getAndConcatenateData(query)
    jobs_object = {"type": "workable", "count": jobs_count, "results": all_jobs}
    return jobs_object


# print(getJobs("frontend"))

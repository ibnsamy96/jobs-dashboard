import requests as rq
from bs4 import BeautifulSoup


def generateSearchPageLink(page_num: int, query: str):
    query_link = f"https://wuzzuf.net/search/jobs/?filters%5Bpost_date%5D%5B0%5D=within_1_week&q={query}&start={page_num}"
    return query_link


def findIsLastPage(jobs_array):
    if len(jobs_array) <= 0:
        return True
    return False


def fetchPageSoup(page_num: int, query: str):
    get_url = rq.get(generateSearchPageLink(page_num, query))
    get_text = get_url.text
    soup = BeautifulSoup(get_text, "html.parser")
    return soup


def fetchAndParsePageJobs(page_num: int, query: str):
    page_jobs = []
    soup = fetchPageSoup(page_num, query)
    h2 = soup.find_all("h2", {"class": "css-m604qf"})
    for h2Element in h2:
        aElement = h2Element.find("a")
        exact_job_href = f'https://wuzzuf.net{aElement.get("href")}'.split("?")[0]
        job_info = {
            "title": aElement.string,
            "href": exact_job_href,
        }
        page_jobs.append(job_info)

    return page_jobs


def getAndConcatenateData(query: str):
    all_jobs = []
    page_num = 0
    maximumNumOfPages = 10  # maximum number of pages to search in
    jobs_count = 0

    while page_num < maximumNumOfPages:
        page_jobs = fetchAndParsePageJobs(page_num, query)
        isLastPage: bool = findIsLastPage(page_jobs)

        if isLastPage:
            break

        jobs_count += len(page_jobs)
        all_jobs.extend(page_jobs)

        page_num += 1

    return jobs_count, all_jobs


def getJobs(query: str):
    jobs_count, all_jobs = getAndConcatenateData(query)
    jobs_object = {"type": "wuzzuf", "count": jobs_count, "results": all_jobs}
    return jobs_object

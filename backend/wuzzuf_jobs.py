import nest_asyncio
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup

nest_asyncio.apply()


def generateSearchPageLink(page_num: int, query: str):
    query_link = f"https://wuzzuf.net/search/jobs/?filters%5Bpost_date%5D%5B0%5D=within_1_week&q={query}&start={page_num}"
    return query_link


def findIsLastPage(jobs_array):
    if len(jobs_array) <= 0:
        return True
    return False


async def fetchPageSoup(page_num: int, query: str):
    async_session = AsyncHTMLSession()
    request = await async_session.get(generateSearchPageLink(page_num, query))
    await request.html.arender(timeout=20)
    body = request.html.find("body")[0]
    soup = BeautifulSoup(body.html, "html.parser")
    return soup



async def fetchAndParsePageJobs(page_num: int, query: str):
    page_jobs = []
    soup = await fetchPageSoup(page_num, query)
    job_elements = soup.find_all("img", {"class": "css-17095x3"})
    h2_elements = soup.find_all("h2", {"class": "css-m604qf"})
    for h2_element in h2_elements:
        print(job_elements)
        # imgElement = job_element.get("a").get("img")
        # print(imgElement.get("src"))
        aElement = h2_element.find("a")
        exact_job_href = f'https://wuzzuf.net{aElement.get("href")}'.split("?")[0]
        job_info = {
            "title": aElement.string,
            "href": exact_job_href,
        }
        page_jobs.append(job_info)

    return page_jobs


async def getAndConcatenateData(query: str):
    all_jobs = []
    page_num = 0
    maximumNumOfPages = 10  # maximum number of pages to search in
    jobs_count = 0

    while page_num < maximumNumOfPages:
        page_jobs = await fetchAndParsePageJobs(page_num, query)
        isLastPage: bool = findIsLastPage(page_jobs)

        if isLastPage:
            break

        jobs_count += len(page_jobs)
        all_jobs.extend(page_jobs)

        page_num += 1

    return jobs_count, all_jobs


async def getJobs(query: str):
    jobs_count, all_jobs = await getAndConcatenateData(query)
    jobs_object = {"type": "wuzzuf", "count": jobs_count, "results": all_jobs}
    return jobs_object

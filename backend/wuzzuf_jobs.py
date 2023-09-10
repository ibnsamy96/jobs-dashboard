import nest_asyncio
import asyncio

import requests
from bs4 import BeautifulSoup

nest_asyncio.apply()


def generateSearchPageLink(page_num: int, query: str):
    query_link = f"https://wuzzuf.net/search/jobs/?filters%5Bpost_date%5D%5B0%5D=within_1_week&q={query}&start={page_num}"
    return query_link


def findIsLastPage(jobs_array):
    if len(jobs_array) <= 0:
        return True
    return False


async def fetchPageSoup(url: str):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup


def createJobObject(**kwargs):

    job = {
        "title": kwargs.get("title"),
        "description": kwargs.get("description"),
        "href": kwargs.get("href"),
        "location": {
            "city": kwargs.get("location_city"),
            "country": kwargs.get("location_country"),
        },
        "company": {
            "name": kwargs.get("company_title"),
            "logo": kwargs.get("company_image"),
            "url": kwargs.get("company_website"),
        },
    }

    return job


def parseJobTitle(job_div):
    return (
        job_div.find("div", {"class": "css-laomuu"}).find("h2").find("a").text.strip()
    )


def parseJobDescription(job_div):
    full_description = ""
    headlines = (
        job_div.find("div", {"class": "css-y4udm8"})
        .find("div", {"class": "css-1lh32fc"})
        .find("a")
    )

    for headline in headlines:
        full_description = headline.text.strip() + " · "

    general_info = (
        job_div.find("div", {"class": "css-y4udm8"})
        .find("div", {"class": "css-1lh32fc"})
        .next_sibling.text.strip()
    )

    full_description += general_info
    return full_description


def parseJobHRef(job_div):
    job_relative_href = (
        job_div.find("div", {"class": "css-laomuu"}).find("h2").find("a").get("href")
    )
    job_abslute_href = f"https://wuzzuf.net{job_relative_href}".split("?")[0]
    return job_abslute_href


def parseLocationCityAndCountry(job_div):
    location = (
        job_div.find("div", {"class": "css-laomuu"})
        .find("div", {"class": "css-d7j1kk"})
        .find("span")
        .text
    )
    location_country = location.split(",")[-1].strip()
    location_city = location.split(",")[-2].strip()

    return location_city, location_country


def parseCompanyTitle(job_div):
    return (
        job_div.find("div", {"class": "css-laomuu"})
        .find("div", {"class": "css-d7j1kk"})
        .find("a")
        .text[:-1]
        .strip()
    )


def parseCompanyWebsite(job_div):
    return (
        job_div.find("div", {"class": "css-laomuu"})
        .find("div", {"class": "css-d7j1kk"})
        .find("a")
        .get("href")
    )


async def fetchAndParsePageJobs(page_num: int, query: str):
    # print("wuzzuf_fetchAndParsePageJobs")
    page_jobs = []
    page_link = generateSearchPageLink(page_num, query)
    print(page_link)
    soup = await fetchPageSoup(url=page_link)
    job_divs = soup.find_all("div", {"class": "css-pkv5jc"})
    for job_div in job_divs:
        title = parseJobTitle(job_div)
        description = parseJobDescription(job_div)
        href = parseJobHRef(job_div)

        location_city, location_country = parseLocationCityAndCountry(job_div)

        company_title = parseCompanyTitle(job_div)
        company_website = parseCompanyWebsite(job_div)

        job_info = createJobObject(
            title=title,
            href=href,
            description=description,
            company_website=company_website,
            company_title=company_title,
            location_city=location_city,
            location_country=location_country,
        )

        page_jobs.append(job_info)

    return page_jobs


async def getAndConcatenateData(query: str):
    import time

    start = time.time()

    all_jobs = []
    page_num = 0
    maximumNumOfPages = 10  # maximum number of pages to search in
    jobs_count = 0

    while page_num < maximumNumOfPages:
        page_jobs = await fetchAndParsePageJobs(page_num, query)

        isLastPage: bool = findIsLastPage(page_jobs)

        now: float = time.time()
        elispated_time = now - start

        if elispated_time > 8 or isLastPage:
            print(elispated_time)
            break

        jobs_count += len(page_jobs)
        all_jobs.extend(page_jobs)

        page_num += 1

    return jobs_count, all_jobs


async def getJobs(query: str):
    print("wuzzuf_getJobs")
    jobs_count, all_jobs = await getAndConcatenateData(query)
    jobs_object = {"type": "wuzzuf", "count": jobs_count, "results": all_jobs}
    print(jobs_object)
    return jobs_object


# asyncio.run(getJobs('frontend'))

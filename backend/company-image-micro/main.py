import nest_asyncio
from fastapi import FastAPI
from pydantic import BaseModel

# from typing import Optional

from bs4 import BeautifulSoup

from requests_futures.sessions import FuturesSession

from concurrent.futures import as_completed
import time

nest_asyncio.apply()
app = FastAPI()


class Company(BaseModel):
    company_title: str
    company_website: str
    company_image: str = None
    page_type: str = None


@app.get("/")
def home():
    return {"message": "Welcome home, son!"}


@app.get("/get-companies-logos")
def getLogos(componies_websites: list[Company]):
    # print(componies_websites)
    companies_images = get_companies_images(componies_websites)
    return companies_images


def parseCompanyImageCP1(company_page_soup):
    return company_page_soup.find("img", {"itemprop": "logo"}).get("src")


def parseCompanyImageCP2(company_page_soup):
    return company_page_soup.find("img", {"title": "Company Logo"}).get("src")


def get_companies_images(componies_websites: list[Company]):
    pages_contents = listToContent(componies_websites)
    componies_images = []
    for page_content in pages_contents:
        try:
            company_page_soup = page_content["soup"]
            # print(company_website)
            if company_page_soup.find_all("html")[0].get("xmlns:jobboard"):
                company_image = parseCompanyImageCP1(company_page_soup)
            else:
                company_image = parseCompanyImageCP2(company_page_soup)

        except:
            company_image = None

        componies_images.append(
            {
                "company_title": page_content["title"],
                "company_website": page_content["url"],
                "company_image": company_image,
                "page_type": page_content["page_type"],
            }
        )
    return componies_images


def listToContent(componies_websites: list[Company]):
    pages_contents = []

    start = time.time()
    session = FuturesSession()

    futures = map(
        lambda company: session.get(dict(company)["company_website"]),
        componies_websites,
    )

    # futures = map(
    #     lambda company: {
    #         "request": session.get(dict(company)["company_website"]),
    #         "title": dict(company)["company_title"],
    #         "url": dict(company)["company_website"],
    #     },
    #     componies_websites,
    # )

    for future in as_completed(futures):
        response = future.result()
        company_info = getPageTitleAndType(
            request_url=response.request.url, componies_websites=componies_websites
        )
        pages_contents.append(
            {
                "title": company_info["title"],
                "url": company_info["url"],
                "page_type": company_info["page_type"],
                "soup": BeautifulSoup(response.content, "html.parser"),
            }
        )

    end = time.time()
    print(end - start)

    return pages_contents


def getPageTitleAndType(request_url, componies_websites: list[Company]):
    url_parts = request_url.split("?")
    url = url_parts[0]
    page_type = url_parts[1].split("=")[-1]
    title = dict(
        list(
            filter(
                lambda company: url == dict(company)["company_website"],
                componies_websites,
            )
        )[0]
    )["company_title"]
    return {"title": title, "url": url, "page_type": page_type}

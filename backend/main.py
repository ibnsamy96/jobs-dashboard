import nest_asyncio
from fastapi import FastAPI
from fastapi.param_functions import Query

import wuzzuf_jobs as wuzzufJ
import workable_jobs as workableJ
import telegram_groups_jobs as telegramGJ

import time

nest_asyncio.apply()
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
async def fetchWuzzuf(query: str):
    print("wuzzuf_api")
    start = time.time()
    wuzzuf_jobs = await wuzzufJ.getJobs(query)
    end = time.time()
    print(end - start)
    return wuzzuf_jobs


@app.get("/workable")
def fetchWorkable(query: str):
    workable_jobs = workableJ.getJobs(query)
    return workable_jobs


@app.get("/telegram/login")
async def loginTelegram(
    phone: str,
    code: str or None = None,
    password: str or None = None,
    phone_code_hash: str or None = None,
):
    phone = f"+{phone}"
    # user_session_string = "1BJWap1wBuxP5Bw8EEUoMxgJoYsJLeUKCsQtOWoq9EazeWjBJluEsM2r3itAB5NRnQE_4viYrIla_VYBvXPO2f41MkIC7Fv058IuR4cVlNCfQWL3dliVwVC3TPNtkupcl1obFzPk6qoydi65SphdDMfWwZ1Sm5wUtfX5_WvusrMua3TIOJ7EL92lCiMWre_oqeQyn4Q1-tGrRsZn6vonUP4AjNnq_6xFJtWkHpzSzr6JoH2DuLCUbh6HUta6gZJZ1USfpuk-BDRibxIfBH3pS91txDvH5PNiWKkt_-Bcbt7VLr5fyzF2SyFe0gtCLgdGTX9au4P-es6Dj2w3HW5zestoCBVTlzks="

    user_string = telegramGJ.init(
        phone_number=phone,
        code=code,
        # user_session_string=user_session_string,
        password=password,
        phone_code_hash=phone_code_hash,
    )
    print({"phone": phone})
    return user_string


# @app.get("/telegram")
# def fetchTelegram(query: str, phone: str):
#     telegram_jobs = telegramGJ.getJobs(query)
#     return telegram_jobs


# wuzzuf_jobs = wuzzufJ.getJobs("front end development")
# workable_jobs = workableJ.getJobs("front end development")

# print(wuzzuf_jobs)
# print(workable_jobs)

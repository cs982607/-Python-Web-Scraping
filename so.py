import requests
from bs4 import BeautifulSoup
#bs4 버전 BeautifulSoup import
# 1. 페이지 가져오기
# 2. requests 만들기
# 3. job 추출하기( 원하는 정보)
URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():

    result = requests.get(URL)
    # 1.페이지 가져오기, requests 만들기
    soup = BeautifulSoup(result.text, "html.parser")
    # 2. BeautifulSoup로 result에 있는 text만 가져오기
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    # 3. soup에 저장된 text 중에 div > class > s-pagination(전체 페이지수) > "a" 찾아 변수저장
    last_page = pages[-2].get_text(strip=True)
    # pages에 저장된 text를 마지막에서 두번째까지만 출력한 후 strip 양끝쪽 공백제거

    return int(last_page)


def extrct_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, loction = html.find("h3").find_all("span", recursive=False)
    # recursive은 같은 클래스명을 전부 가져오는것을 방지 가장 위에 있는것만 가져오기
    company = company.get_text(strip=True)
    loction = loction.get_text(strip=True).strip("-").strip(" \r")
    # strip은 양끝쪽에 있는 공백과 특수문자 제거와 지정한 문자제거,strip(" \r") 한칸 제거(\n)과 같은 기능
    job_id = html['data-jobid']
    return {
        'title': title,
        'company': company,
        "loction": loction,
        'apply_link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def extrct_jobs(last_page):
    # return 값 last_page를 인자로 받기
    jobs = []  # jobs 리스트만들기
    for page in range(last_page):
        # range 배열로 page에 변수 저장
        print (f"Scraping SO: Page : {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        # 전체 페이지수 받기
        soup = BeautifulSoup(result.text, "html.parser")
        # result 값을 text만 받기
        results = soup.find_all("div", {"class": "-job"})
        # soup에서 사용값 찾기
        for result in results:
            # for문으로 results 값에 저장된 값 result값에 새로저장
            # for문에 있는 조건으로만 저장
            job = extrct_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extrct_jobs(last_page)
    return jobs

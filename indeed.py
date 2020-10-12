import requests 
from bs4 import BeautifulSoup
#bs4 버전 BeautifulSoup import

LIMIT = 50
URL= f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_page():
  result = requests.get(URL)
#url 주소 변수 저장
  soup = BeautifulSoup(result.text, "html.parser")
# BeautifulSoup 변수 설정 indeed site에서 text 가져오기
  
  pagination = soup.find("div", {"class": "pagination"})
#pagination , indeed_soup.find 명령어로 찾기
#div 로 사용된 class 

  links = pagination.find_all('a')
#pagination에서 찾은 div, class 중에서 'a'(anchor) 찾기

  pages = [] # 비어있는 리스트 작성
  for link in links[:-1] : 
    pages.append(int(link.string)) 
    # find("span")
    #Links 에 있는 각 anchor의 span 안에 있는 string만 검색 
    #link 에 변수 저장, 
    # string 을 int 로 변경 // 마지막 next 는 int로 변환이 안되니 마지막 직전까지 저장 
# pages = pages[0:-1]
# [-1]spans 은 모두 가져오되 마지막 것은 제외
# [0:5] 으로 할 경우 첫5개의 item 불러오기
# [0:-1] 처음부터 마지막 요소까지 실행 ( 마지막 직전 ) 
# print (pages[-1]) 
# 마지막 숫자 출력
  max_page = pages[-1]
  return max_page

def extract_job(html) :
      title = html.find("h2", {"class" : "title"}).find("a")["title"]
      # for result in results 는 result(전체)에서 results(soup에서 검색한 값)을 가져온값 
      # title 변수는 result 값에서 h2에 있는 class 에 있는 title 안에 있는 a(anchor)에 안에 있는 title 을 저장
      company = html.find("span", {"class" : "company"})
      # result 에서 span 안에 있는 class 안에 있는 company 를 company 변수 저장
      if company :
        company_anchor =  company.find("a")
        # company 변수에 있는 a(anchor)을 찾아 변수 저장
        if company_anchor is not None:
          company =  str(company_anchor.string)
          # 만약 company_anchor 에서 찾은 변수에 'a'가 있다면 'a'출력 후 company 에 저장 
        else:
          company = str(company.string)
          # company_anchor에서 찾은 변수에 'a'가 없다면 string만 출력 후 company에 저장
          company = company.strip()
      # 위에 함수에 의해 저장된 company를 실행 strip은 사이드에 있는 부분이 없어짐
          location = html.find("div" , {"class" : "recJobLoc"}) ["data-rc-loc"]
          job_id = html["data-jk"]
          return{ 'title' : title, 'company' : company , 'location' : location , 'link' : f"https://www.indeed.com/viewjob?jk={job_id} "}
          



def extrac_jobs(last_page) :
  jobs = []
  for page in range (last_page) :
    print (f"Scraping Indeed: Page : {page}")
    result = requests.get(f"{URL}&start={page*LIMIT} ")
  # requests.get 로 전체 페이지 가져오기
    soup = BeautifulSoup(result.text, "html.parser")
  # soup 로 페이지 text 로 가져오기
    results = soup.find_all("div" , {"class": 
    "jobsearch-SerpJobCard"})   
  # results 값에 soup 로 가져온 text 에서 div,class안에 있는 jobsearch-SerpJobCard 값 가져오기
    for result in results : 
        job = extract_job(result)
        jobs.append (job)
  return jobs


def get_jobs() :
  last_page = get_last_page()
  jobs = extrac_jobs(last_page)
  return jobs
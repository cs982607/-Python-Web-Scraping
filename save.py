import csv


def save_to_file(jobs):
    file = open("jobs.csv", mode='w')
    # 파일오픈(생성) jobs.csv , mode writer(쓰기만가능))
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    # 상단에 목록 쓰기
    for job in jobs:
        writer.writerow(list(job.values()))
        # for 문으로 jobs값을 받아 job에 저장 
        # jobs 값에 values값만 list 로 저장
    
    return

import csv
import json
import time
from dataclasses import dataclass
from itertools import cycle
from flask import Flask, request

import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring

app = Flask(__name__)

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

@app.route('/health', methods=['GET'])
def health():
    return "UP"


@app.route('/vacancy', methods=['POST'])
def vacancy_controller():
    request_json = request.get_json(silent=True)
    id = request_json['id']
    if not id:
        return "Vacancy id must not be empty", 400
    # resumeId = "0bbf67e600034e469c00000dc94e3365464a59"
    return parse_vacancy(id)



def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:30]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)

    return proxies


def invokeWithProxy(url):
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    # Get a proxy from the pool
    proxy = next(proxy_pool)
    while True:
        try:
            return requests.get(url, headers=headers, proxies={"http://": proxy, "https://": proxy})
        except Exception as e:
            print(e)
            # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
            # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
            print("Skipping. Connnection error")
            proxy = next(proxy_pool)


@dataclass
class Resume:
    companyName: str
    title: str
    salary: str
    experience: str
    employeeMode: str
    tags: []
    description: str
    link: str


class MockNode:
    text: str = ''

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration


def saveSearch(func):
    try:
        var = func()
        if len(var) == 0:
            return MockNode()
        return var
    except Exception:
        return MockNode()

def parse_vacancy(id):
    return parse_vacancy_internal(f"https://hh.ru/vacancy/{id}")

def parse_vacancy_internal(link):
    # link = "https://hh.ru/vacancy/48502563?from=vacancy_search_list&query=java"
    resumePage = invokeWithProxy(link)
    # resumePage = requests.get(link, headers=headers)

    parsedPage = BeautifulSoup(resumePage.content, "html.parser")
    companyName = saveSearch(lambda: parsedPage.find("a", class_='vacancy-company-name').find("span"))
    title = saveSearch(lambda: parsedPage.find("h1", class_='bloko-header-1'))
    salary = saveSearch(lambda: parsedPage.find("span", attrs={"data-qa": "bloko-header-2"}))
    experience = saveSearch(lambda: parsedPage.find("span", attrs={"data-qa": "vacancy-experience"}))
    employeeMode = saveSearch(lambda: parsedPage.find("p", attrs={"data-qa": "vacancy-view-employment-mode"}))
    tagList = saveSearch(lambda: parsedPage.findAll("span", attrs={"data-qa": "bloko-tag__text"}))
    description = saveSearch(lambda: parsedPage.find("div", class_='vacancy-description'))
    resume = Resume(
        companyName=companyName.text,
        title=title.text,
        salary=salary.text,
        experience=experience.text,
        employeeMode=employeeMode.text,
        tags=[i.text for i in tagList],
        description=description.text,
        link=link
    )
    return resume.__dict__
    # writer.writerow(resume.__dict__)
    # time.sleep(0.5)
    # print(f'{link} proceeded')

def parse_vacancies_from_file(file_name):
    with open(file_name, 'r', newline='') as txtFile:
        ids = txtFile.read().splitlines()
        # ids = ['06e738e2000209e5b100000dc94e736a437068']
        res = [parse_vacancy(i) for i in ids if parse_vacancy(i) is not None]
        # print(res)
        print(json.dumps(res, indent=4, ensure_ascii=False))

def main():
    with open('manager_resumes.csv', 'a', newline='') as csvfile:
        fieldnames = ['companyName', 'title', 'salary', 'experience', 'employeeMode', 'tags', 'description', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        max_pages = 39
        links = []
        for page_num in range(1, max_pages):
            print(f"page {page_num}")
            URL = f"https://hh.ru/search/vacancy?text=Руководитель&page={page_num}"

            page = invokeWithProxy(URL)
            # page = requests.get(URL, headers=headers)

            soup = BeautifulSoup(page.content, "html.parser")
            # print(soup.prettify())
            vacancies = soup.findAll("div", class_='vacancy-serp-item')
            # print(vacancies.len)
            for vacancy in vacancies:
                link = vacancy.find("a", attrs={"data-qa": "vacancy-serp__vacancy-title"})
                links.append(link['href'])
        for linkNum in range(1, len(links)):
            print(f"start {linkNum}  from {len(links)}")
            parse_vacancy(links[linkNum], writer)


if __name__ == "__main__":
    # parse_vacancies_from_file("vacancies.txt")
    app.run(host='0.0.0.0')

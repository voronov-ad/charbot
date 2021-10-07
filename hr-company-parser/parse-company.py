from operator import itemgetter

import requests
from bs4 import BeautifulSoup
from flask import Flask, request


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


class Company:
    name: str
    vacancies: int
    area: []
    city: str
    description: str
    link: str

    def __init__(self, name, vacancies, ara, city, description, link):
        self.name = name
        self.vacancies = vacancies
        self.area = ara
        self.city = city
        self.description = description
        self.link = link


app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    return "UP"

@app.route('/company', methods=['POST'])
def parseCompany():
    request_json= request.get_json(silent=True)
    name = request_json['name']
    if not name:
        return "Company name must not be empty", 400
    # companyName = "IBReal"
    URL = f"https://hh.ru/employers_list?query={name}&areaId=113"

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    page = requests.get(URL, headers=headers)
    # if page.status_code !=
    soup = BeautifulSoup(page.content, "html.parser")
    companyList = soup.find("td", class_="b-companylist")
    try:
        childs = companyList.findChildren(recursive=False)
    except Exception as e:
        print("не найдены компании: " + companyName)
        exit()
    companies = []
    for child in childs:
        link = "https://hh.ru" + child.find("a")['href']
        count = int(child.find("em").text)
        companies.append({"name": "", "link": link, "count": count})
    print(URL)
    print(f"Всего компаний {len(companies)}")
    companies_sorted = sorted(companies, key=itemgetter('count'), reverse=True)
    print(*companies_sorted, sep="\n")
    companyLink = companies_sorted[0]['link']
    print(f"Взяли c самым бошльшим количеством вакансий {companyLink}")
    companyPage = requests.get(companyLink, headers=headers)
    companySoup = BeautifulSoup(companyPage.content, "html.parser")
    place = saveSearch(lambda: companySoup.find("div", class_="employer-sidebar-block"))
    vanaciesLink = saveSearch(
        lambda: companySoup.find("a", attrs={"data-qa": "employer-page__employer-vacancies-link"}))
    areasOfActivity = saveSearch(lambda: companySoup.find("div", text="Сферы деятельности").find_next_sibling())
    description = saveSearch(lambda: companySoup.find("div", class_="company-description"))
    try:
        vacancies = int(vanaciesLink.text.split(sep=' ')[0])
    except:
        vacancies = 0
    company = Company(name=place.text, vacancies=vacancies,
                      ara=[i.lower() for i in areasOfActivity.text.split(',')],
                      city=place.text, description=description.text,
                      link=companyLink)
    return company.__dict__

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
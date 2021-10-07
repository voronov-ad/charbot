import json

import requests
from flask import Flask, request
from bs4 import BeautifulSoup


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


# app = Flask(__name__)


class LastWork:
    position: str


class Employee:
    name: str
    age: int
    date_of_birth: str
    address: str
    metro: str
    position: str
    salary: str
    specializations:[]
    specialization_category: str
    exprerience: str
    last_work: LastWork
    work_place_count: int
    skills: []
    has_education: bool
    languages: []
    link: str

    def __init__(self, name, age, date_of_birth, address, metro, position, salary, specialization,specialization_category, exprerience,
                 last_work,
                 work_place_count, skills, has_education, languages, link):
        self.name = name
        self.age = age
        self.date_of_birth = date_of_birth
        self.address = address
        self.metro = metro
        self.position = position
        self.salary = salary
        self.specialization = specialization
        self.specialization_category = specialization_category
        self.exprerience = exprerience
        self.last_work = last_work
        self.work_place_count = work_place_count
        self.skills = skills
        self.has_education = has_education
        self.languages = languages
        self.link = link


def parse_employee(id):
    URL = f"https://hh.ru/resume/{id}"

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    print(URL)

    # cookies = {'hhtoken': 'G5WXUWnSUnlmqdfdKaIwMXJZsEtp'}

    page = requests.get(URL, headers=headers)
    print("Status" + str(page.status_code))
    if page.status_code == 403:
        print("Unauthorised")
        return
    soup = BeautifulSoup(page.content, "html.parser")
    errorNode = soup.find("div", class_="error")
    if errorNode is not None:
        print("Captcha")
        return
    # print(soup)
    nameNode = saveSearch(lambda: soup.find("h2", attrs={"data-qa": "resume-personal-name"}))
    ageNode = saveSearch(lambda: soup.find("span", attrs={"data-qa": "resume-personal-age"}))
    ageNode = saveSearch(lambda: soup.find("span", attrs={"data-qa": "resume-personal-age"}))
    dateOfBirth = saveSearch(lambda: soup.find("span", attrs={"data-qa": "resume-personal-birthday"}))
    address = saveSearch(lambda: soup.find("span", attrs={"data-qa": "resume-personal-address"}))
    metro = saveSearch(lambda: soup.find("span", attrs={"data-qa": "resume-personal-metro"}))
    salary = saveSearch(lambda: soup.find("span", attrs={"data-qa": "resume-block-salary"}))
    headerTitle = saveSearch(lambda: soup.find("div", class_="resume-header-title"))
    movementParams = headerTitle.findAll("p")[1].text.split(',')
    if "не" in movementParams[0]:
        movement = False
    else:
        movement = True
    position = saveSearch(lambda: soup.find("span", class_="resume-block__title-text"))
    specialization_category = saveSearch(lambda: soup.find("span", attrs={"data-qa": "resume-block-specialization-category"}))
    specializations_nodes = soup.findAll("li", attrs={"data-qa": "resume-block-position-specialization"})
    specializations = []
    for node in specializations_nodes:
        for i in node.text.split(','):
            stripped = i.strip()
            lowered = stripped.lower()
            specializations.append(lowered)

    resumeBlock = saveSearch(lambda: soup.find("div", attrs={"data-qa": "resume-block-experience"}))
    exprerience = saveSearch(lambda: resumeBlock.find("span", class_="resume-block__title-text"))

    experienceBlock = soup.find("div", attrs={"data-qa": "resume-block-experience"})
    works = []
    lastWorkPlacePosition = MockNode
    if experienceBlock is not None:
        works = experienceBlock.findAll("div", class_="resume-block-item-gap")
        lastWork = works[0]
        lastWorkPlacePosition = lastWork.find("div", attrs={"data-qa": "resume-block-experience-position"})

    skillsNode = soup.find("div", attrs={"data-qa": "skills-table"})
    tags = skillsNode.findAll("span", attrs={"data-qa": "bloko-tag__text"})

    education = soup.findAll("div", attrs={"data-qa": "resume-block-education-item"})
    hasEducation = False
    if len(education) > 0:
        hasEducation = True

    languages = soup.findAll("p", attrs={"data-qa": "resume-block-language-item"})
    employee = Employee(name=nameNode.text, age=ageNode.text, date_of_birth=dateOfBirth.text, address=address.text,
                        metro=metro.text, position=position.text, salary=salary.text,
                        specialization_category=specialization_category.text, specialization=specializations,
                        exprerience=exprerience.text,
                        last_work=lastWorkPlacePosition.text, work_place_count=str(len(works)),
                        skills=[i.text for i in tags], has_education=hasEducation,
                        languages=[i.text for i in languages],
                        link=URL
                        )
    return employee.__dict__


@app.route('/health', methods=['GET'])
def health():
    return "UP"


@app.route('/employee', methods=['POST'])
def employee_controller():
    request_json = request.get_json(silent=True)
    id = request_json['id']
    if not id:
        return "Employee id must not be empty", 400
    # resumeId = "0bbf67e600034e469c00000dc94e3365464a59"
    return parse_employee(id)

def main():
    with open('links.txt', 'r', newline='') as txtFile:
        ids = txtFile.read().splitlines()
        # ids = ['06e738e2000209e5b100000dc94e736a437068']
        res = [parse_employee(i) for i in ids if parse_employee(i) is not None]
        # print(res)
        print(json.dumps(res, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # main()

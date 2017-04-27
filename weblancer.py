
import urllib.request
from bs4 import BeautifulSoup

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse(html):
    soup = BeautifulSoup(html)
    table = soup.find('div', class_='container-fluid cols_table show_visited')

    projects = []  #хранилице проектов

    for row in table.find_all('div', class_='row')[1:]:
        col_title = row.find_all('div', class_='col-sm-7 col-lg-8')

        projects.append({
            'title': col_title[0].a.text
        })

    for project in projects:
        print(project)


def main():
    parse(get_html('http://weblancer.net/jobs'))

if __name__ == '__main__':
    main()

import csv
import urllib.request
from bs4 import BeautifulSoup

BASE_URL = 'http://weblancer.net/jobs'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def get_page_count(html):
    soup = BeautifulSoup(html)
    pagination = soup.find('ul', class_='pagination')
    return int(pagination.find_all('a')[-1].get('href')[12:])

def parse(html):
    soup = BeautifulSoup(html)
    table = soup.find('div', class_='container-fluid cols_table show_visited')

    projects = []  #хранилице проектов

    for row in table.find_all('div', class_='row')[1:]:
        col_title = row.find('div', class_='col-sm-7 col-lg-8')
        col_category = row.find('div', class_='col-xs-12 text-muted')
        col_price = row.find('div', class_='col-sm-1 amount title')

        projects.append({
            'title': col_title.a.text,
            'categories': [category.text for category in col_category.find_all('a', class_='text-muted')],
            'price': col_price.text.strip()
        })

    return projects

def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Проекты', 'Категории', 'Цена'))

        for project in projects:
            writer.writerow((project['title'], ', '.join(project['categories']), project['price']))

def main():
    page_count = get_page_count(get_html(BASE_URL))
    print('Всего найдено страниц %d' % page_count)

    projects = []
    projects.extend(parse(get_html(BASE_URL)))

    for page in range(2, 5):
        print('Парсинг %d%%' % (page / page_count * 100))
        projects.extend(parse(get_html(BASE_URL + '?page=%d' % page)))

    save(projects, 'projects.csv')


if __name__ == '__main__':
    main()
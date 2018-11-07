import random
import time
from fake_useragent import UserAgent
import requests
from lxml import etree
from bs4 import BeautifulSoup
import json
from datetime import datetime
from openpyxl import Workbook


def get_courses_list(xml_url):
    courses_xml = requests.get(
        xml_url,
        UserAgent().chrome,
        timeout=(1, 30),
        proxies={'http': 'http://10.10.1.10:3128'}
    )
    root = etree.fromstring(courses_xml.text.encode('utf-8'))
    courses_urls_list = []
    for elements in root.getchildren():
        for url in elements.getchildren():
            courses_urls_list.append(url.text)
    return courses_urls_list


def get_course_info(course_url):
    title = None
    language = None
    json_info = None
    rating = None
    start_date = None
    weeks = None
    while not title or not language or not json_info or not rating:
        secs = round(random.random()*5)
        time.sleep(secs)
        response = requests.get(
            course_url,
            UserAgent().chrome,
            timeout=(1, 30),
            proxies={'http': 'http://10.10.1.10:3128'}
        )
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title
        if title:
            title = title.string.split('|')[0].strip()
        language = soup.find_all('h4')
        if language:
            language = language[-1].contents[0]
        json_info = soup.find('script', attrs={'type': 'application/ld+json'})
        if json_info:
            json_info = json_info.contents[0].strip()
            json_graph = json.loads(json_info)['@graph']
            start_date = json_graph[1]['hasCourseInstance']['startDate']
            end_date = json_graph[1]['hasCourseInstance']['endDate']
            weeks = round((datetime.strptime(end_date,
                                             '%Y-%m-%d') - datetime.strptime(
                start_date, '%Y-%m-%d')).days / 7)
        rating = soup.find(
            'span',
            class_='H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 '
                   'm-l-1s m-r-1 m-b-0')
        if rating:
            rating = rating.contents[0]
    return title, language, start_date, weeks, rating


def output_courses_info_to_xlsx(courses_urls_list, filepath):
    wb = Workbook()
    ws = wb.active
    for url in courses_urls_list:
        title, language, start_date, weeks, rating = get_course_info(url)
        print('{}, {}, {}, {}, {}'.format(
            title,
            language,
            start_date,
            weeks,
            rating
        ))
        ws.append([title, language, start_date, weeks, rating])
    return wb.save(filepath)


if __name__ == '__main__':
    coursera_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    filepath = 'sample.xlsx'
    num_urls = 5
    courses_list = get_courses_list(coursera_url)
    print('\nGetting {} random urls from coursera.org ... '.format(num_urls))
    rand_courses_urls = random.sample(courses_list, num_urls)
    for url in rand_courses_urls:
        print(url)
    print('\nGetting these courses info from coursera.org '
          '(Title, Language, Start date, Weeks, Rating)')
    output_courses_info_to_xlsx(rand_courses_urls, filepath)
    print('\nWriting data to {} ... '.format(filepath))
    print('\nThe file was saved successfully in the current directory.')

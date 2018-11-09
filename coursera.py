import argparse
import random
import time
from fake_useragent import UserAgent
import requests
from lxml import etree
from bs4 import BeautifulSoup
import json
from datetime import datetime
from openpyxl import Workbook


def get_args_parser():
    parser = argparse.ArgumentParser(description='Coursera Dump')
    parser.add_argument(
        'urls',
        help='how many urls to parse from coursera',
        type=int
    )
    parser.add_argument(
        'filename',
        help='name of xlsx - file to save results',
        type=str
    )
    args = parser.parse_args()
    return args


def get_courses_urls(xml_url):
    courses_xml = requests.get(xml_url, UserAgent().chrome, timeout=(1, 30))
    root = etree.fromstring(courses_xml.text.encode('utf-8'))
    courses_urls_list = []
    for elements in root.getchildren():
        for url in elements.getchildren():
            courses_urls_list.append(url.text)
    return courses_urls_list


def get_course_info(course_url):
    start_date = None
    weeks = None
    response = requests.get(course_url, UserAgent().chrome, timeout=(1, 30))
    secs = 5 + round(random.random() * 25)
    time.sleep(secs)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title
    if title:
        title = title.string.split('|')[0].strip()
    language = soup.find_all('h4')
    if language:
        language = language[-1].contents[0]
    else:
        language = None
    json_info = soup.find('script', attrs={'type': 'application/ld+json'})
    if json_info:
        json_info = json_info.contents[0].strip()
        json_graph = json.loads(json_info)['@graph']
        start_date = json_graph[1]['hasCourseInstance']['startDate']
        start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = json_graph[1]['hasCourseInstance']['endDate']
        end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d')
        weeks = round((end_date_formatted - start_date_formatted).days / 7)
    rating = soup.find('div', class_='CourseRating')
    if rating:
        rating = rating.contents[1].string
    return {
        'title': title,
        'language': language,
        'start_date': start_date,
        'weeks': weeks,
        'rating': rating
    }


def output_courses_info_to_xlsx(courses_urls_list, worksheet):
    for url in courses_urls_list:
        worksheet.append(list(get_course_info(url).values()))
    return worksheet


if __name__ == '__main__':
    user_args = get_args_parser()
    num_urls = user_args.urls
    filepath = user_args.filename
    coursera_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_list = get_courses_urls(coursera_url)
    print('\nGetting {} random urls from coursera.org ... '.format(num_urls))
    rand_courses_urls = random.sample(courses_list, num_urls)
    print('\nGetting courses info from coursera.org...')
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(['title', 'language', 'start date', 'weeks', 'rating'])
    output_courses_info_to_xlsx(rand_courses_urls, worksheet)
    print('\nWriting data to {} ... '.format(filepath))
    workbook.save(filepath)
    print('\nThe file was saved successfully in the current directory.')

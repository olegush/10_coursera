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


def get_courses_urls(xml_tree):
    courses_urls_list = []
    for elements in xml_tree.getchildren():
        for url in elements.getchildren():
            courses_urls_list.append(url.text)
    return courses_urls_list


def get_course_info(soup):
    start_date = None
    weeks = None
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
        course_info_graph = json.loads(json_info)['@graph']
        start_date = course_info_graph[1]['hasCourseInstance']['startDate']
        start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = course_info_graph[1]['hasCourseInstance']['endDate']
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


if __name__ == '__main__':
    user_args = get_args_parser()
    num_urls = user_args.urls
    filepath = user_args.filename
    coursera_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_urls_response = requests.get(
        coursera_url,
        UserAgent().chrome,
        timeout=(1, 30)
    )
    courses_xml_tree = etree.fromstring(courses_urls_response.content)
    courses_list = get_courses_urls(courses_xml_tree)
    print('\nGetting {} random urls from coursera.org ... '.format(num_urls))
    rand_courses_urls = random.sample(courses_list, num_urls)
    print('\nGetting courses info from coursera.org...')
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(['title', 'language', 'start date', 'weeks', 'rating'])
    for course_url in rand_courses_urls:
        time.sleep(5 + round(random.random() * 25))
        courses_response = requests.get(
            course_url,
            UserAgent().chrome,
            timeout=(1, 30)
        )
        courses_response.encoding = 'utf-8'
        soup = BeautifulSoup(courses_response.text, 'html.parser')
        course_info_dict = get_course_info(soup)
        worksheet.append([
            course_info_dict['title'],
            course_info_dict['language'],
            course_info_dict['start_date'],
            course_info_dict['weeks'],
            course_info_dict['rating']
        ])
    print('\nWriting data to {} ... '.format(filepath))
    workbook.save(filepath)
    print('\nThe file was saved successfully in the current directory.')

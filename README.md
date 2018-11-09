# Coursera Dump

The script parses xml feed [from coursera.org](https://www.coursera.org/sitemap~www~courses.xml), and gets random courses urls from it. Then, the script parses every url and get some info: title, language, start_date, weeks, rating of the course. Finally, this dump saves to xlsx-file in the current directory.


# How to Install

Before you start please install python packages from **requirements.txt**.

```bash

$ pip install -r requirements.txt
```


# Quickstart

Run **coursera.py** with arguments.

Example of script launch on Linux, Python 3.7:

```bash

$ python coursera.py 5 sample.xlsx

Getting 5 random urls from coursera.org ...

Getting courses info from coursera.org

Writing data to sample.xlsx ...

The file was saved successfully.
```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

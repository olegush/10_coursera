# Coursera Dump

The script parses xml feed [from coursera.org](https://www.coursera.org/sitemap~www~courses.xml), and gets random courses urls from it. Then, the script parses every url and get some info: title, language, start_date, weeks, rating of the course. Finally, this dump saves to xlsx-file in the current directory.


# How to Install

Before you start please install python packages from **requirements.txt**.

```bash

$ pip install -r requirements.txt
```


# Quickstart

Just run **coursera.py** 

Example of script launch on Linux, Python 3.7:

```bash

$ python coursera.py

Getting 5 random urls from coursera.org ...
https://www.coursera.org/learn/scientist
https://www.coursera.org/learn/audio-signal-processing
https://www.coursera.org/learn/reinforcement-learning-in-finance
https://www.coursera.org/learn/organisational-design-know-your-organisation
https://www.coursera.org/learn/asymmetric-crypto

Getting these courses info from coursera.org (Title, Language, Start date, Weeks, Rating)
On Being a Scientist, English, 2018-11-12, 10, 4.4
Audio Signal Processing for Music Applications, English, 2018-12-24, 11, 4.8
Reinforcement Learning in Finance, English, 2018-11-05, 5, 3.3
Organisational design: Know your organisation, English, 2018-11-05, 7, 5.0
Asymmetric Cryptography and Key Management, English, 2018-11-05, 5, 4.6

Writing data to sample.xlsx ...

The file was saved successfully in the current directory.
```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

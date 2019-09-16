from requests import get
from bs4 import BeautifulSoup as BS
import logging
from datetime import datetime as dt
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# intialize the sections from the website that i would like to obtain
sections = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'l', 'm', 'n', 'p', 'r', 's', 't', 'w')
# initialize an array to store each webpage
course_sources = set({})
for section in sections:

        # get the page contents
        source = get(
            "https://utsc.calendar.utoronto.ca/list-of-courses/" + section).text
        page = BS(source, 'lxml')
        logging.info('LOADED PAGE ' + section.upper())

        # get the course elements
        courses = page.find_all(
            'div', class_='view-content')[4].find_all('div')

        # obtain every href
        for course in courses:
                # for every course on the page get and store its page href in the set
                href_loc = course.find('a')
                if href_loc is not None:
                        href = href_loc['href']
                        course_sources.add(href)
                        logging.info("OBTAINED " +
                                     href[-8:].upper() + " PAGE")

        logging.info("OBTAINED ALL " + section.upper() + " COURSES")

# open a file to write to csv
time = str(dt.now()).replace(' ', '_').replace(':', '-')
time = time[:time.find('.')]
file = time + '-Prereqs.csv'
logging.info("OPENED FILE: " + file)

with open(file, 'w') as f:
        f.write('Course,Prerequisite\n')
        logging.info("WROTE CSV HEADER")

        # loop through the courses set obtaining each courses pre reqs
        for link in course_sources:
                # get course page
                url = "https://utsc.calendar.utoronto.ca" + link
                course_page = get(url)
                content = BS(course_page.text)

                # get prereqs
                prereq_container = content.find(
                    'div', class_="field-name-field-prerequisite1")

                # check if the course has any listed prereqs
                if(prereq_container is not None):
                        prereqs = prereq_container.find('p').text
                else:
                        prereqs = "None"

                prereqs = prereqs.replace(',', '')
                # add the course info to the csv
                course_name = link[-8:]
                try:
                        f.write(course_name + ',' + prereqs + "\n")
                        logging.info("WROTE " +
                                     course_name.upper() + " PREREQUISITES")
                except:
                        logging.critical(
                            "FAILED: " + course_name + ', ' + prereqs)
logging.info("COMPLETE")

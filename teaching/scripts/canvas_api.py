'''
Abe Handler's command-line scripts for accessing the canvas API

Setup:
1. Go to https://canvas.colorado.edu/profile/settings and click "+ New Access Token"
2. in your local shell, run export CANVAS_TOKEN="my_secret_token"
3. Install the python client $pip install canvasapi
'''


import os
import argparse
from datetime import datetime
from canvasapi import Canvas


def get_api():

    # Canvas API URL
    API_URL = "https://canvas.colorado.edu"
    # Canvas API key
    API_KEY = os.environ['CANVAS_TOKEN']

    # Initialize a new Canvas object
    return Canvas(API_URL, API_KEY)


def createInClassAssignment(courseNo, date):

    course = canvas.get_course(COURSES[courseNo])

    group_id = COURSE2INCLASS[courseNo]

    date = datetime.strptime(date, '%Y%m%d')

    print("[*] Creating in-class assignment {} for {}".format(courseNo, date))

    new_assignment = course.create_assignment({
        'name': 'In-class assignment, {}'.format(date.strftime("%b %d")),
        'published': True,
        'unlock_at': date.strftime('%Y-%m-%d') + "T09:00:00",
        'lock_at': date.strftime('%Y-%m-%d') + "T17:00:00",
        "assignment_group_id": group_id,
        "points_possible": 3
    })


if __name__ == "__main__":
    canvas = get_api()

    # map CU names to names in Canvas
    COURSES = {"4604": 62561}

    # map course to in-class assignment groups
    COURSE2INCLASS = {"4604": "149100"}

    parser = argparse.ArgumentParser()
    parser.add_argument('--course', help='INFO course number, e.g. 4604')

    parser.add_argument('--inClass', help='pass a date in YYYYMMDD to create in-class assignment, e.g. 20200824')

    args = parser.parse_args()

    # course = canvas.get_course(COURSES["4604"])
    # print(course.name)
    # course.create_quiz({"title": "test"})

    # createInClassAssignment(courseNo="4604", date="20200826")

    try:
        datetime.strptime(args.inClass, '%Y%m%d')
        createInClassAssignment(courseNo=args.course, date=args.inClass)
    except ValueError:
        print("[*] The argument inClass needs to match the format YYYYMMDD. Won't make assignment.")

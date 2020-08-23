'''
Command-line interface to the canvas API.
- This will modify your canvas courses
- Start with your sandbox course when learning
- Mostly just a wrapper over https://github.com/ucfopen/canvasapi

Setup for CU users:
1. Go to https://canvas.colorado.edu/profile/settings and click "+ New Access Token"
2. in your local shell, run export CANVAS_TOKEN="my_secret_token"
3. Install the python client $pip install canvasapi

Questions and contact:
abram.handler@gmail.com
www.abehandler.com

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


def createInClassAssignment(courseNo, date, published=False):

    course = canvas.get_course(COURSES[courseNo])

    group_id = COURSE2INCLASS[courseNo]

    date = datetime.strptime(date, '%Y%m%d')

    print("[*] Creating in-class assignment {} for {}".format(courseNo, date))

    course.create_assignment({
        'name': 'In-class assignment, {}'.format(date.strftime("%b %d")),
        'published': published,
        'unlock_at': date.strftime('%Y-%m-%d') + "T09:00:00",
        'lock_at': date.strftime('%Y-%m-%d') + "T17:00:00",
        "assignment_group_id": group_id,
        "points_possible": 3
    })

    print("   - Added assignment to {}".format(course.name))


if __name__ == "__main__":
    canvas = get_api()

    # map CU names to names in Canvas
    COURSES = {"4604": 62561, "sandbox": 62535}

    # map course to in-class assignment groups
    COURSE2INCLASS = {"4604": "149100"}

    parser = argparse.ArgumentParser()

    parser.add_argument('--course', default='sandbox', help='INFO course number, e.g. 4604')

    parser.add_argument('--quiz', '-quiz', dest='quiz', default='false', action='store_true', help='Use this flag to create a quiz')

    parser.add_argument('--assignment', '-assignment', dest='assignment', default='false', action='store_true', help='Use this flag to create an assignment')

    parser.add_argument('--due', help='pass a date in YYYYMMDD for the due date, e.g. 20200824')

    parser.add_argument('--publish', dest='publish', default='false', action='store_true', help='Use this flag to immediately publish the assignment')

    args = parser.parse_args()

    if(args.quiz):
        course = canvas.get_course(COURSES[args.course])
        course.create_quiz({'title': "test"})
    '''
    try:
        datetime.strptime(args.dueDate, '%Y%m%d')
        createInClassAssignment(courseNo=args.course, date=args.dueDate)
    except ValueError:
        print("[*] The argument inClass needs to match the format YYYYMMDD. Won't make assignment.")
    '''
'''
Proof of concept for accessing the canvas API

1. Go to https://canvas.colorado.edu/profile/settings and click "+ New Access Token"
2. in your local shell, run export CANVAS_TOKEN="my_secret_token"
3. Install the python client $pip install canvasapi
'''


# Import the Canvas class
import os
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

    new_assignment = course.create_assignment({
        'name': 'In-class assignment, {}'.format(date.strftime("%b %d")),
        'published': True,
        "assignment_group_id": group_id
    })


if __name__ == "__main__":
    canvas = get_api()

    # map CU names to names in Canvas
    COURSES = {"4604": 62561}

    # map course to in-class assignment groups
    COURSE2INCLASS = {"4604": "149100"}

    course = canvas.get_course(COURSES["4604"])

    # print(course.name)
    # course.create_quiz({"title": "test"})

    createInClassAssignment(courseNo="4604", date="20200826")

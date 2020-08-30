'''
An opinionated command-line interface to the canvas API.
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

To make an API call when logged into canvas do this 

https://canvas.colorado.edu/api/v1/courses/62535/assignment_groups

'''


import time
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

# update an assignment
# https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update


def create_in_class_assignment(courseNo, due, name, published=False):

    course = canvas.get_course(COURSES[courseNo])

    due = datetime.strptime(due, '%Y%m%d')

    print("[*] Creating in-class assignment {} for {}".format(courseNo, due))

    course.create_assignment({
        'name': name,
        'published': published,
        'due_at': due.strftime('%Y-%m-%d') + "T23:59:00",
        "points_possible": 3
    })

    print("   - Added assignment to {}".format(course.name))


def init_course_files(course_number):
    # See https://github.com/ucfopen/canvasapi/issues/415

    course = canvas.get_course(course_number)

    # Create a folder in canvas
    for week in range(1, 17):
        print("[*] Init folders week {}".format(week))
        parent = "/week{}/".format(week)
        course.create_folder(name='quiz_files', parent_folder_path=parent)
        course.create_folder(name='assignment_files', parent_folder_path=parent)
        course.create_folder(name='other_files', parent_folder_path=parent)


if __name__ == "__main__":
    canvas = get_api()

    # map CU names to names in Canvas
    COURSES = {"4604": 62561, "sandbox": 62535, "2301": 62559}

    # map course to in-class assignment groups
    COURSE2INCLASS = {"4604": "149100"}

    COURSE2CLASSTIME = {"4604": "T12:40:00", "sandbox": "T12:40:00"}

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '-course', '--course', default='sandbox', help='INFO course number, e.g. 4604')

    parser.add_argument('-init_files', '--init_files', dest='init_files', default=False, action='store_true', help='Use this flag to init the course files on Canvas')

    parser.add_argument('--quiz', '-quiz', dest='quiz', default='false', action='store_true', help='Use this flag to create a quiz')

    parser.add_argument('--assignment', '-assignment', dest='assignment', default='false', action='store_true', help='Use this flag to create an assignment')

    parser.add_argument('-a', '-attachments', '--attachments', nargs='+', help='Input a list of globs; matching files will be uploaded', required=False)

    parser.add_argument('-d', '-due', '--due', help='pass a date in YYYYMMDD for the due date, e.g. 20200824')

    parser.add_argument('-n', '-name', '--name', help='the name of the quiz or assignment')

    parser.add_argument('-time_limit', '--time_limit', default=10, help='time limit, in minutes')

    parser.add_argument('--publish', dest='publish', default='false', action='store_true', help='Use this flag to immediately publish the assignment')

    args = parser.parse_args()

    # test out overrides
    '''
    course = canvas.get_course(COURSES["sandbox"])
    assignment = course.get_assignment(826690)
    KEEGAN = 107996488
    assignment.edit(assignment={"name":"tex", "assignment_overrides": [{"student_ids": KEEGAN, "due_at": "2012-07-01T23:59:00-06:00"}]})
    '''

    print(args)

    if(args.quiz):
        course = canvas.get_course(COURSES[args.course])
        course.create_quiz({'title': args.name,
                            'published': args.publish,
                            'time_limit': args.time_limit,
                            "due_at": args.due + "T" + COURSE2CLASSTIME[args.course]})

    '''
    if(args.assignment):
        try:
            datetime.strptime(args.due, '%Y%m%d')
            create_in_class_assignment(courseNo=args.course, due=args.due, name=args.name)
        except ValueError:
            print("[*] The argument inClass needs to match the format YYYYMMDD. Won't make assignment.")
    '''

    if(args.init_files):
        init_course_files(COURSES[args.course])

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

    course = canvas.get_course(CU2Canvas[courseNo])

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


def get_student_names2_ids(course_no):
    '''
    courseno = a canvas course number
    Returns a dictionary of names 2 student ids for this course
    note that maps student names to *canvas* student IDs
    '''
    out = {}
    course = canvas.get_course(course_no)
    for student in course.get_recent_students():
        out[student.name] = student.id
    return out


if __name__ == "__main__":
    canvas = get_api()

    # Map CU course names to Canvas course names
    CU2Canvas = {"4604": 62561, "sandbox": 62535, "2301": 62559}

    # map course to in-class assignment groups
    COURSE2INCLASS = {"4604": "149100"}

    Course2Classtime = {"4604": "T12:40:00", "sandbox": "T12:40:00"}

    names2ids = {}
    for coursename, courseno in CU2Canvas.items():
        names2ids[coursename] = get_student_names2_ids(CU2Canvas[coursename])

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '-course', '--course', default='sandbox', help='INFO course number, e.g. 4604')

    parser.add_argument('-init_files', '--init_files', dest='init_files', default=False, action='store_true', help='Use this flag to init the course files on Canvas')

    parser.add_argument('-q', '-quiz', '--quiz', dest='quiz', default=False, action='store_true', help='Use this flag to create a quiz')

    parser.add_argument('-a', '-assignment', '--assignment', dest='assignment', default='false', action='store_true', help='Use this flag to create an assignment')

    parser.add_argument('-attachments', '--attachments', nargs='+', help='Input a list of globs; matching files will be uploaded', required=False)

    parser.add_argument('-d', '-due', '--due', help='pass a date in YYYYMMDD for the due date, e.g. 20200824')

    parser.add_argument('-n', '-name', '--name', help='the name of the quiz or assignment')

    parser.add_argument('-w', '-week', '--week', dest='week', type=int)

    parser.add_argument('-p', '-points', '--points', dest='points', default=10, type=int)

    parser.add_argument('-u', '-upload', '--upload', help='Uploads all files in this folder to canvas. ', dest='upload', type=str)

    parser.add_argument('-time_limit', '--time_limit', default=10, help='time limit, in minutes')

    parser.add_argument('--publish', dest='publish', default='false', action='store_true', help='Use this flag to immediately publish the assignment')

    args = parser.parse_args()

    # test out overrides

    print(args)

    course = canvas.get_course(CU2Canvas["sandbox"])
    assignment = course.get_assignment(826690)

    extra_time = ['Jason Zietz', 'Brian Keegan']
    ids = [names2ids[args.course][i] for i in extra_time]

    for quiz in course.get_quizzes():
        for id_ in ids:
            quiz.set_extensions([{'user_id': id_, 'extra_time': 60}])

    import os
    os._exit(0)

    if(args.quiz):
        course = canvas.get_course(CU2Canvas[args.course])
        course.create_quiz({'title': args.name,
                            'published': args.publish,
                            'time_limit': args.time_limit,
                            "points_possible": args.points,
                            "due_at": args.due + "T" + Course2Classtime[args.course]})

    if(args.assignment):
        try:
            datetime.strptime(args.due, '%Y%m%d')
            create_in_class_assignment(courseNo=args.course, due=args.due, name=args.name)
        except ValueError:
            print("[*] The argument inClass needs to match the format YYYYMMDD. Won't make assignment.")

    if(args.init_files):
        init_course_files(CU2Canvas[args.course])

    if args.upload is not None:

        def get_week_folder(course_no, week_no):
            course = canvas.get_course(CU2Canvas[args.course])
            for f in course.get_folders():
                if f.name == "week{}".format(args.week):
                    return f

        folder = get_week_folder(CU2Canvas[args.course], args.week)

        print(folder)
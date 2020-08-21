'''
Proof of concept for accessing the canvas API

1. Go to https://canvas.colorado.edu/profile/settings and click "+ New Access Token"
2. in your local shell, run export CANVAS_TOKEN="my_secret_token"
3. Install the python client $pip install canvasapi
'''


# Import the Canvas class
import os
from canvasapi import Canvas

# Canvas API URL
API_URL = "https://canvas.colorado.edu"
# Canvas API key
API_KEY = os.environ['CANVAS_TOKEN']

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

course = canvas.get_course(62561)

print(course.name)

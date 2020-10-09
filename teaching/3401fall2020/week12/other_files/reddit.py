import praw
import os

client_id = os.environ['client_id']
client_secret = os.environ['secret']

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent='my_user_agent')

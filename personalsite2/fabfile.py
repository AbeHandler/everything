from fabric.api import *

def build():
    local("bundle exec jekyll build")

def serve():
    local("bundle exec jekyll serve")

def deploy():
    build()
    local("aws s3 cp _site s3://www.abehandler.com  --recursive")
    local('aws cloudfront create-invalidation --distribution-id E2NDQN6OXXN3XW --paths "/*"')

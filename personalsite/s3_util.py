import sys
import os

# in bash run ... 
# $CDN_DISTRIBUTION_ID="check aws here"
# $export CDN_DISTRIBUTION_ID



with open("upload.sh", "w") as of:
    for lno, line in enumerate(sys.stdin):
        print(lno)
        out = "aws s3 cp " + line.strip("\n") + " " + "s3://www.abehandler.com/" + line.replace("_site/", "").replace("\n", "") + " --acl public-read --content-type text/html"
        print(out)
        of.write(out + "\n")
    of.write("aws s3 cp images s3://www.abehandler.com/images --recursive  --acl public-read" + "\n")
    of.write("aws s3 cp _site/index.html s3://www.abehandler.com/index.html --acl public-read" + "\n")
    of.write('aws cloudfront create-invalidation --distribution-id ' + os.environ['CDN_DISTRIBUTION_ID'] + ' --paths "/*"' + "\n")

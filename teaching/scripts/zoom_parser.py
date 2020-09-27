import sys
from jinja2 import Template


template = '''
<ul>
<li><a href="{{link}}">Sep 25</a> (PW: {{pw}})</li>
</ul>
'''

template = Template(template)
link = None

for o in list(sys.stdin):
    if "cuboulder" in o:
        link = o 
    if "Passcode" in o:
        o = o.replace("Access Passcode", "").replace(":", "")
        pw = o 
        print(o)


print(template.render(pw=pw, link=link))

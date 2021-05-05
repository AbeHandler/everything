import spacy
import en_core_web_sm
import markupsafe
from spacy import displacy
from jinja2 import Template
from flask import Flask
from jinja2 import Environment, PackageLoader, select_autoescape
from flask import Flask, url_for
from flask import render_template

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

app = Flask(__name__)

@app.route("/hi")
def templates(): 

    template = env.get_template('child.html')

    nlp = en_core_web_sm.load()

    text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    markup = displacy.render(doc, style="ent")
 
    output = template.render(markup=markupsafe.Markup(markup))

    return output


@app.route('/')
def hello_world():

    nlp = en_core_web_sm.load()

    text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    markup = displacy.render(doc, style="ent")
 
    with open('template.html') as file_:
        template = Template(file_.read())
    output = template.render(markup=markup)

    return (output)

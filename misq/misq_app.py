import json
import spacy
import en_core_web_sm
import markupsafe
from spacy import displacy
from jinja2 import Template
from flask import Flask
from jinja2 import Environment, PackageLoader, select_autoescape
from flask import Flask, url_for
from flask import render_template
import altair as alt
from vega_datasets import data


env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

app = Flask(__name__)

@app.route("/")
def templates(): 

    template = env.get_template('child.html')

    nlp = en_core_web_sm.load()

    text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    markup = displacy.render(doc, style="ent")
 
    chart = alt.Chart(data.cars.url).mark_point().encode(
        x='Horsepower:Q',
        y='Miles_per_Gallon:Q',
        color='Origin:N'
    )

    chart = json.loads(chart.to_json())
    chart = json.dumps(chart) 

    output = template.render(markup=markupsafe.Markup(markup), chart=chart)

    return output

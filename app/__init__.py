import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

LIGHTNING_TALK_URL = "https://www.youtube.com/embed/rj4qNrLJUL8?si=FG0wF17vJHMiCPcs"

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="Andrew Lai", url=os.getenv("URL"), lightning_talk_url=LIGHTNING_TALK_URL)

@app.route('/work')
def work():
    return render_template('work.html', title="Work", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))

@app.route('/map')
def map():
    return render_template('map.html', title="Map", url=os.getenv("URL"))
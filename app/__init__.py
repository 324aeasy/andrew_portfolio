import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

LIGHTNING_TALK_URL = "https://www.youtube.com/embed/rj4qNrLJUL8?si=FG0wF17vJHMiCPcs"
MAP_URL = "https://www.google.com/maps/d/u/0/embed?mid=1b-h0riTTWJiwujiu2AjCJCo1p9us2XI&ehbc=2E312F"

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="Andrew Lai", url=os.getenv("URL"), lightning_talk_url=LIGHTNING_TALK_URL)

@app.route('/work')
def work():
    # sample `works` as a list of dicts: each dict has keys role, company, dates, description
    works = [
        {
            "role": "Production Engineering Fellow",
            "company": "Meta and Major League Hacking",
            "dates": "2026 - Present",
            "description": "<p>Developing a Flask personal portfolio website adhering to DevOps practices, with a focus on CI/CD, containerization, cloud deployment via DigitalOcean, and automated testing.</p>"
        },
        {
            "role": "Data Engineer",
            "company": "Deloitte",
            "dates": "2022 - 2024",
            "description": "<p>Shipped multiple $500k+ enterprise-scale technical implementation and migrations for clients in banking, insurance, and healthcare sectors. Also the Google Cloud Alliance lead for Omnia AI, hosting monthly townhalls.</p>"
        },
        {
            "role": "Data Science/ML Intern",
            "company": "Axcessiom Technologies",
            "dates": "2021 - 2022",
            "description": "<p>Built speech and facial recognition models to enable disabled drivers to operate auxiliary vehicle functions (e.g., turn signals, windshield wipers) with voice commands or facial gestures.</p>"
        }
    ]

    education = [
        {
            "degree": "M.S. Computer Science",
            "university": "University of Texas at Austin",
            "dates": "2025 - Present",
            "description": "<p>Coursework: Structure and Implementation of Programming Languages, Deep Learning</p>"
        },
        {
            "degree": "B.S. Software Engineering",
            "university": "Ontario Tech University",
            "dates": "2018 - 2022",
            "description": "<p>GPA: 4.06/4.3</p>"
        }
    ]

    return render_template('work.html', title="Work", url=os.getenv("URL"), works=works, education=education)

@app.route('/hobbies')
def hobbies():
    hobbies = [
        {
            "image": "./static/img/hie_shrine.jpg",
            "label": "Finding Hidden Gems",
            "description": "Inari gates at Hie Shrine. Like Fushimi Inari but no crowds :)"
        },
        {
            "image": "./static/img/mt_si.jpg",
            "label": "Hiking", 
            "description": "Beat the 30° incline on the the Kamikaze trail at Mount Si in Seattle, WA."
        },
        {
            "image": "./static/img/mt_takao.jpg",
            "label": "Mt. Takao",
            "description": "The mountain locals frequent for a quick nature escape and Mt. Fuji views on a clear day"
        },
    ]
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"), hobbies=hobbies)

@app.route('/map')
def map():
    return render_template('map.html', title="Map", url=os.getenv("URL",), map_url=MAP_URL)
import os
import re
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
import hashlib
from playhouse.shortcuts import model_to_dict

EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

load_dotenv()

app = Flask(__name__)
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared',uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306)

class TimelinePost(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

app.config['LIGHTNING_TALK_URL'] = os.getenv("LIGHTNING_TALK_URL")
app.config['MAP_URL'] = os.getenv("MAP_URL")

@app.route('/')
def index():
    return render_template('index.html', title="Andrew Lai", url=os.getenv("URL"), lightning_talk_url=app.config['LIGHTNING_TALK_URL'])

@app.route('/work')
def work():
    # sample `works` as a list of dicts: each dict has keys role, company, dates, description
    works = [
        {
            "role": "Production Engineering Fellow",
            "company": "Meta and Major League Hacking",
            "dates": "2026 - Present",
            "description": "<p>Developing a Flask personal portfolio website adhering to DevOps practices, with a focus on CI/CD, containerization, cloud deployment with DigitalOcean, and automated testing.</p>"
        },
        {
            "role": "Data Engineer Consultant",
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
            "description": "Inari gates at Hie Shrine. Like Fushimi Inari but no crowds :)",
            "caption_class": "caption-cyan"
        },
        {
            "image": "./static/img/mt_si.jpg",
            "label": "Hiking", 
            "description": "Mount Si in Seattle, WA",
            "caption_class": "caption-blue"
        },
        {
            "image": "./static/img/ndc_podium.jpg",
            "label": "Volunteering at Conferences",
            "description": "NDC Toronto 2026",
            "caption_class": "caption-white"
        },
    ]
    
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"), hobbies=hobbies)

@app.route('/map')
def map():
    return render_template('map.html', title="Map", url=os.getenv("URL",), map_url=app.config['MAP_URL'])

@app.route('/timeline')
def timeline():
    timeline_posts = [
        model_to_dict(p)
        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
    ]

    for post in timeline_posts:
        normalized_email = post['email'].strip().lower().encode('utf-8')
        email_hash = hashlib.md5(normalized_email).hexdigest()
        post['gravatar_url'] = f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=512"

    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"), timeline_posts=timeline_posts)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    content = request.form.get('content', '').strip()

    if not name:
        return {'error': 'Invalid name'}, 400
    if not EMAIL_PATTERN.match(email):
        return {'error': 'Invalid email'}, 400
    if not content:
        return {'error': 'Invalid content'}, 400

    max_post_id = TimelinePost.select(fn.MAX(TimelinePost.id)).scalar()
    post_id = 0 if max_post_id is None else max_post_id + 1

    timeline_post = TimelinePost.create(id=post_id, name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():
    post_id = request.args.get('id') or request.form.get('id')

    if post_id is None:
        return {'error': 'id is required'}, 400

    try:
        post_id = int(post_id)
    except ValueError:
        return {'error': 'id must be an integer'}, 400

    deleted_count = TimelinePost.delete().where(TimelinePost.id == post_id).execute()

    if deleted_count == 0:
        return {'error': 'timeline post not found'}, 404

    return {'deleted': post_id}

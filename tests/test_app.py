import unittest
import os
from http.client import responses

os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['LIGHTNING_TALK_URL'] = 'https://www.youtube.com/embed/rj4qNrLJUL8?si=FG0wF17vJHMiCPcs'
        app.config['MAP_URL'] = 'https://www.google.com/maps/d/u/0/embed?mid=1b-h0riTTWJiwujiu2AjCJCo1p9us2XI&ehbc=2E312F'
    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.content_type.startswith("text/html")
        html = response.get_data(as_text=True)
        #edited this from MLH fellow to name to match changes made to website template
        #general content tests
        assert "<title>Andrew Lai</title>" in html
        assert app.config['LIGHTNING_TALK_URL'] in html
        assert "About" in html
        #nav bar tests
        assert 'href="/work"' in html
        assert 'href="/map"' in html
        assert 'href="/timeline"' in html

    def test_timeline(self):
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        #tests 1 post made to timeline
        postA = self.client.post('/api/timeline_post', data={
            "name" : "MLH Fellow Number 1",
            "email": "myemail@notmeta.com",
            "content":"Im a MLH fellow! Yippee"
        })
        assert postA.status_code == 200
        assert postA.is_json
        postMade = postA.get_json()
        assert postMade["name"] == "MLH Fellow Number 1"
        assert postMade["email"] == "myemail@notmeta.com"
        assert postMade["content"] == "Im a MLH fellow! Yippee"
        assert "id" in postMade
        #tests a second post made
        postB = self.client.post('/api/timeline_post', data={
            "name" : "MLH Fellow Number 2",
            "email": "anotheremail@gmail.com",
            "content":"Im also a MLH fellow! Yippee"
        })
        assert postB.status_code == 200
        assert postB.is_json
        postMade2 = postB.get_json()
        assert postMade2["name"] == "MLH Fellow Number 2"
        assert postMade2["email"] == "anotheremail@gmail.com"
        assert postMade2["content"] == "Im also a MLH fellow! Yippee"
        assert "id" in postMade
        #tests receiving posts back on /api/timeline endpoint
        apiGetReq = self.client.get('/api/timeline_post')
        assert apiGetReq.status_code == 200
        assert apiGetReq.is_json
        json = apiGetReq.get_json()
        assert "timeline_posts" in json
        timeline_posts = json["timeline_posts"]
        assert len(timeline_posts) == 2
        assert timeline_posts[0]["name"] == "MLH Fellow Number 2"
        assert timeline_posts[1]["name"] == "MLH Fellow Number 1"
        assert timeline_posts[1]["email"] == "myemail@notmeta.com"
        assert timeline_posts[0]["email"] =="anotheremail@gmail.com"
        #tests regular timeline page
        timelineReq = self.client.get('/timeline')
        assert timelineReq.status_code == 200
        html = timelineReq.get_data(as_text=True)
        assert "Add Timeline Post" in html
        assert "anotheremail@gmail.com" in html
        assert "Timeline" in html
        assert "MLH Fellow Number 1" in html
        #checking nav bar again bc why not
        assert 'href="/work"' in html
        assert 'href="/map"' in html
        assert 'href="/timeline"' in html
    def test_malformed_timeline_post(self):
        #Post request missing name
        response = self.client.post("/api/timeline_post", data={
            "email":"josh@example.com",
            "content":"This post has a missing name...invalid!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        #Post request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name":"John Doe",
            "email":"john@example.com",
            "content":""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        #Post request with malformed email
        response = self.client.post("/api/timeline_post", data={
            "name":"John Doe",
            "email":"12345 My Home Address",
            "content":"Hey! That's not an email!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html



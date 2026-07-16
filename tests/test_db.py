import hashlib
import unittest
from peewee import *
from playhouse.shortcuts import model_to_dict

from app import TimelinePost

MODELS = [TimelinePost]

#use an in memory SQLite for tests
test_db = SqliteDatabase(':memory:')
class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of all models, we don't need to recursively bind dependencies
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
    def tearDown(self):
        # Not strictly needed since SQLite in memory dbs only live for the duration of the connection, and in the next step we close the connection, but good practice regardless
        test_db.drop_tables(MODELS)
        #Close connection to db
        test_db.close()
    def test_timeline_post(self):
        #Create 2 timeline posts
        first_post = TimelinePost.create(name="John Doe",email="john@example.com",content="Hello world, I\'m John!")
        assert first_post.id == 1
        second_post = TimelinePost.create(name="Jane Doe", email="jane@example.com", content = "Hi everyone, I\'m Jane!")
        assert second_post.id == 2

        timeline_posts = [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]

        #second timeline post testing (Jane)
        second_timeline_post = timeline_posts[0]
        assert second_timeline_post['id'] == second_post.id
        assert second_timeline_post['name'] == second_post.name
        assert second_timeline_post['email'] == second_post.email
        assert second_timeline_post['content'] == second_post.content

        #first timeline post testing (John)
        first_timeline_post = timeline_posts[1]
        assert first_timeline_post['id'] == first_post.id
        assert first_timeline_post['name'] == first_post.name
        assert first_timeline_post['email'] == first_post.email
        assert first_timeline_post['content'] == first_post.content

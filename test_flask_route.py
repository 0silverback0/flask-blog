from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOST'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTest(TestCase):
    """Test for views in app.py"""

    def setUp(self):
        """add a user to database"""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="gary", last_name='the snail')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title='test', content='this is a test', created_at='1-1-21', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post = post
        self.post_id = post.id

    
    def tearDown(self):
        """ clean up after test """
        db.session.rollback()

    def test_home_view(self):
        with app.test_client() as client:
            res = client.get('/')

            self.assertEqual(res.status_code, 302)

    def test_users_view(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_users_new(self):
        with app.test_client() as client:
            res = client.get('/user/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_users_new_post(self):
        with app.test_client() as client:
            test_data = {"first": "fred", "last": "flintstone", "img": "www.spongbob.com"}
            res = client.post('/users/new', data=test_data, follow_redirects=True)
            # html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)

    def test_users_new_details(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)

    def test_users_post_new(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}/post/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Add Post for gary the snail</h1>', html)

    def test_users_post_method(self):
        with app.test_client() as client:
            test_data = {"title": self.post.title, "content": self.post.content, "created_at": self.post.content, "user_id": self.user_id}
            res = client.post(f'/users/{self.user_id}/posts/new', data=test_data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<li> <a href="/posts/{self.post_id}">test</a> </li>', html)

    def test_post_post_id(self):
        with app.test_client() as client:
            res = client.get(f'/posts/{self.post.id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<h1>{self.post.title}</h1>', html)

    def test_post_post_id_edit(self):
        with app.test_client() as client:
            res = client.get(f'/posts/{self.post.id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Edit Post</h1>', html)

    def test_post_post_id_edit_post_req(self):
        with app.test_client() as client:
            test_data = {"title": "test", "content": "this is a test"}
            res = client.post(f'/posts/{self.post.id}/edit', data=test_data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>test</h1>', html)
            self.assertIn('<p>this is a test</p>', html)
            

    




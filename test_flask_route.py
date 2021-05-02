from unittest import TestCase

from app import app
from models import db, User

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

        User.query.delete()

        user = User(first_name="gary", last_name='the snail')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
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


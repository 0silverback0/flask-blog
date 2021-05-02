from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name='marz', last_name='Gibbs', img_url=' https://bit.ly/3tQncTZ')
u2 = User(first_name='Trina', last_name='Moore', img_url=' https://bit.ly/3tQncTZ')
u3 = User(first_name='Deja', last_name='Sky', img_url=' https://bit.ly/3tQncTZ')
u4 = User(first_name='Darius', last_name='fast boy')
u5 = User(first_name='Angel', last_name='Fish')
u6 = User(first_name='Trey', last_name='Pound', img_url=' https://bit.ly/3sOENuj')

db.session.add_all([u1,u2,u3,u4,u5,u6])
db.session.commit()

p1 = Post(title='test', content='this is a test', user_id=1)
p2 = Post(title='test 2', content='this is test 2', user_id=2)
p3 = Post(title='test 3', content='another test ', user_id=3)
p4 = Post(title='test 4', content='testing', user_id=4)
p5 = Post(title='test 5', content='this is a stick up', user_id=1)

db.session.add_all([p1, p2, p3, p4, p5])
db.session.commit()
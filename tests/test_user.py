import unittest
from app import create_app
from app.models import db, User
from utils.auth import generate_token

class TestUser(unittest.TestCase):
  
  def setUp(self):
    self.app = create_app("TestingConfig")
    self.user = User(name="test_user", username="testing", email="test@test.com", password="test")
    with self.app.app_context():
      db.drop_all()
      db.create_all()
      db.session.add(self.user)
      db.session.commit()
      self.token = generate_token(1)
    self.client = self.app.test_client()
    
  def test_create_user(self):
    user_payload = {
      "name": "John Doe",
      "username": "jdoe2020",
      "email": "jdoe@test.com",
      "password": "test"
    }

    response = self.client.post("/users/", json=user_payload)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json["name"], "John Doe")
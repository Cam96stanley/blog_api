import unittest
from app import create_app
from app.models import db, User
from utils.auth import generate_token, hash_password

class TestUser(unittest.TestCase):
  
  def setUp(self):
    self.app = create_app("TestingConfig")
    self.user = User(name="test_user", username="testing", email="test@test.com", password=hash_password("test"))
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

  def test_invalid_creation(self):
    user_payload = {
      "name": "John Doe",
      "email": "test1@test.com",
      "password": "test"
    }
    
    response = self.client.post("/users/", json=user_payload)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json["errors"]["username"][0], "Missing data for required field.")
  
  
  def test_login_user(self):
    credentials = {
      "email": "test@test.com",
      "password": "test"
    }
    
    response = self.client.post("/users/login", json=credentials)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json["status"], "success")
    
    
  def invalid_test_login(self):
    credentials = {
      "email": "bad_email@test.com",
      "password": "bad_pw"
    }
    
    response = self.client.post("/users/login", json=credentials)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json["error"], "Invalid email or password")
    
    
  def get_token(self):
    credentials = {
      "email": "test@test.com",
      "password": "test"
    }
    
    response = self.client.post("/users/login", json=credentials)
    return response.json["token"]
    
    
  def test_update_user(self):
    update_payload = {
      "name": "tesssst",
      "email": "test1@test.com"
    }
    
    token = self.get_token()
    headers = {"Authorization": "Bearer " + token}
    
    response = self.client.patch("/users/me", json=update_payload, headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json["name"], "tesssst")
    self.assertEqual(response.json["email"], "test1@test.com")
    

  
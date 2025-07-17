import unittest
from app import create_app
from app.models import db, Blog, User
from utils.auth import generate_token, hash_password

class TestBlog(unittest.TestCase):
  
  def setUp(self):
    self.app = create_app("TestingConfig")
    self.user = User(name="test_user", username="testing", email="test@test.com", password=hash_password("test"))
    self.blog = Blog(title="Test Title", body="test test test", author_id=1)
    with self.app.app_context():
      db.drop_all()
      db.create_all()
      db.session.add(self.user)
      db.session.add(self.blog)
      db.session.commit()
      self.token = generate_token(1)
    self.client = self.app.test_client()
  
  def get_token(self):
    credentials = {
      "email": "test@test.com",
      "password": "test"
    }
    
    response = self.client.post("/users/login", json=credentials)
    return response.json["token"]
  
  
  def test_create_blog(self):
    blog = {
      "title": "Test",
      "body": "test test test"
    }
    
    headers = {"Authorization": "Bearer " + self.get_token()}
    
    response = self.client.post("/blogs/", json=blog, headers=headers)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json["title"], "Test")
    
    
  def test_invalid_creation(self):
    blog = {
      "body": "test test test"
    }
    
    headers={"Authorization": "Bearer " + self.get_token()}
    
    response = self.client.post("/blogs/", json=blog, headers=headers)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json["errors"]["title"][0], "Missing data for required field.")
  
  
  def test_get_all_blogs(self):
    response = self.client.get("/blogs/")
    self.assertEqual(response.status_code, 200)
  
  
  def test_get_single_blog(self):
    response = self.client.get("/blogs/1")
    self.assertEqual(response.status_code, 200)
    
    
  def test_invalid_get_single_blog(self):
    response = self.client.get("/blogs/2")
    self.assertEqual(response.status_code, 404)
    

  def test_update_blog(self):
    update_blog = {
      "title": "TestTest"
    }
    
    headers = {"Authorization": "Bearer " + self.get_token()}
    
    response = self.client.patch("/blogs/1", json=update_blog, headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json["title"], "TestTest")

    
  def test_invalid_update_blog(self):
    update_blog = {
      "title": "TestTest"
    }
    
    response = self.client.patch("/blogs/1", json=update_blog)
    self.assertEqual(response.status_code, 401)
    
    
  def test_toggle_archive(self):
    
    headers = {"Authorization": "Bearer " + self.get_token()}
    
    response = self.client.patch("/blogs/1/archive", headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json["message"], "Blog has been archived")
    
    
  def test_invalid_archive(self):
    response = self.client.patch("/blogs/1/archive")
    self.assertEqual(response.status_code, 401)
import unittest
from app import create_app
from app.models import db, Blog, User, Comment
from utils.auth import generate_token, hash_password

class TestComment(unittest.TestCase):
  
  def setUp(self):
    self.app = create_app("TestingConfig")
    self.user = User(name="test_user", username="testing", email="test@test.com", password=hash_password("test"))
    self.blog = Blog(title="Test Title", body="test test test", author_id=1)
    self.comment = Comment(content="blah blah blah", post_id=1, user_id=1)
    with self.app.app_context():
      db.drop_all()
      db.create_all()
      db.session.add(self.user)
      db.session.add(self.blog)
      db.session.add(self.comment)
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
    
  def test_create_comment(self):
    comment_payload = {
      "content": "test test",
    }
    
    headers = {"Authorization": "Bearer " + self.get_token()}
    
    response = self.client.post("/blogs/1/comments", json=comment_payload, headers=headers)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json["content"], "test test")
    
    
  def test_invalid_creation(self):
    comment_payload = {
      "content": "test"
    }
    
    response = self.client.post("/blogs/1/comments", json=comment_payload)
    self.assertEqual(response.status_code, 401)
    
    
  def test_get_blog_comments(self):
    response = self.client.get("/blogs/1/comments")
    self.assertEqual(response.status_code, 200)
    
    
  def test_update_comment(self):
    comment_payload = {
      "content": "tessssssst"
    }
    
    headers = {"Authorization": "Bearer " + self.get_token()}
    
    response = self.client.patch("/blogs/1/comments/1", json=comment_payload, headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json["content"], "tessssssst")
    
    
  def test_invalid_comment(self):
    comment_payload = {
      "content": "tessst"
    }
    
    response = self.client.patch("/blogs/1/comments/1", json=comment_payload)
    self.assertEqual(response.status_code, 401)
    
    
  def test_toggle_comment_archive(self):
    headers = {"Authorization": "Bearer " + self.get_token()}
    
    response = self.client.patch("/blogs/1/comments/1/archive", headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json["message"], "Comment archived")
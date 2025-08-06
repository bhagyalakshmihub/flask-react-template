import unittest
import json
from main import app, db, Comment

class CommentApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_comment(self):
        response = self.app.post('/comments', json={
            'task_id': 1,
            'content': 'Test comment'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('comment', data)
        self.assertEqual(data['comment']['content'], 'Test comment')

    def test_get_comments(self):
        # First, add a comment
        self.app.post('/comments', json={'task_id': 1, 'content': 'Read comment'})
        
        # Now, get the comment
        response = self.app.get('/comments')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]['content'], 'Read comment')

    def test_update_comment(self):
        # Add comment
        post_res = self.app.post('/comments', json={'task_id': 1, 'content': 'Old'})
        comment_id = json.loads(post_res.data)['comment']['id']

        # Update it
        response = self.app.put(f'/comments/{comment_id}', json={'content': 'Updated'})
        self.assertEqual(response.status_code, 200)
        updated = json.loads(response.data)
        self.assertEqual(updated['comment']['content'], 'Updated')

    def test_delete_comment(self):
        # Add comment
        post_res = self.app.post('/comments', json={'task_id': 1, 'content': 'Delete me'})
        comment_id = json.loads(post_res.data)['comment']['id']

        # Delete it
        response = self.app.delete(f'/comments/{comment_id}')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('message', result)

if __name__ == '__main__':
    unittest.main()

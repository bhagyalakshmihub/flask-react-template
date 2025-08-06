import json
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, db

from models.comment_model import Comment

# This sets up a testing client and a temporary DB
@pytest.fixture(autouse=True)
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client


def test_add_comment(client):
    response = client.post('/comments', json={
        'task_id': 1,
        'content': 'Test comment'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Comment added'

def test_get_comments(client):
    client.post('/comments', json={
        'task_id': 2,
        'content': 'Another comment'
    })
    response = client.get('/comments')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['content'] == 'Another comment'

def test_update_comment(client):
    client.post('/comments', json={
        'task_id': 3,
        'content': 'To be updated'
    })
    response = client.put('/comments/1', json={
        'content': 'Updated!'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Comment updated'

def test_delete_comment(client):
    client.post('/comments', json={
        'task_id': 4,
        'content': 'To be deleted'
    })
    response = client.delete('/comments/1')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Comment deleted'

from flask import Flask, request, jsonify
from models.comment_model import db, Comment
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 👈 Add this line

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 👇 This line creates the database on first run
with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return 'Backend is working! ✅'
# Create a comment
@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    new_comment = Comment(task_id=data['task_id'], content=data['content'])
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({
        'message': 'Comment added',
        'comment': {
            'id': new_comment.id,
            'task_id': new_comment.task_id,
            'content': new_comment.content
        }
    }), 201


# Read all comments
@app.route('/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    return jsonify([{'id': c.id, 'task_id': c.task_id, 'content': c.content} for c in comments])

# Update a comment
@app.route('/comments/<int:id>', methods=['PUT'])
def update_comment(id):
    data = request.get_json()
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    comment.content = data['content']
    db.session.commit()

    return jsonify({
        'message': 'Comment updated',
        'comment': {
            'id': comment.id,
            'task_id': comment.task_id,
            'content': comment.content
        }
    })


# Delete a comment
@app.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'})
if __name__ == '__main__':
    app.run(debug=True)

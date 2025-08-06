import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Comments.css'; // Optional styling file if needed

type Comment = {
  id: number;
  task_id: number;
  content: string;
};

const Comments: React.FC = () => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);

  // Fetch comments from backend
  const fetchComments = async () => {
    try {
      const response = await axios.get<Comment[]>(
        'http://localhost:5000/comments',
      );
      setComments(response.data);
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };

  // Add or Update comment
  const handleSubmit = async () => {
    if (!newComment.trim()) return;

    try {
      if (editingId !== null) {
        // Edit mode
        await axios.put(`http://localhost:5000/comments/${editingId}`, {
          content: newComment,
        });
        setEditingId(null);
      } else {
        // Add new
        await axios.post('http://localhost:5000/comments', {
          task_id: Date.now(),
          content: newComment,
        });
      }

      setNewComment('');
      fetchComments();
    } catch (error) {
      console.error('Error submitting comment:', error);
    }
  };

  // Delete a comment
  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`http://localhost:5000/comments/${id}`);
      fetchComments();
    } catch (error) {
      console.error('Error deleting comment:', error);
    }
  };

  // Load comment into input for editing
  const handleEdit = (comment: Comment) => {
    setNewComment(comment.content);
    setEditingId(comment.id);
  };

  useEffect(() => {
    fetchComments();
  }, []);

  return (
    <div className="comment-container">
      <h2>💬 Comments</h2>

      <div className="input-section">
        <input
          type="text"
          placeholder="Write comment..."
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
        />
        <button onClick={handleSubmit}>
          {editingId !== null ? 'Update' : 'Add'}
        </button>
      </div>

      <ul className="comment-list">
        {comments.map((comment) => (
          <li key={comment.id} className="comment-item">
            <span>{comment.content}</span>
            <div className="comment-buttons">
              <button onClick={() => handleEdit(comment)}>✏️</button>
              <button onClick={() => handleDelete(comment.id)}>🗑️</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Comments;

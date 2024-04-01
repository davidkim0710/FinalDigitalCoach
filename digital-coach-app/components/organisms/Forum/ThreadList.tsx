import React, { useState } from 'react';
import Card from '@App/components/atoms/Card';
import ForumService from './forumapi'; // Import ForumService
import { Button, TextField } from '@mui/material';
import EditThreadForm from './EditThreadForm'; // Import EditThreadForm
import useAuthContext from '@App/lib/auth/AuthContext';

function ThreadList({ threads, setLoading }) {
  const { currentUser } = useAuthContext();
  const [editThreadId, setEditThreadId] = useState(null);
  const [newComment, setNewComment] = useState('');
  const currentUserName = currentUser._document.data.value.mapValue.fields.name.stringValue;

  const handleEdit = (threadId) => {
    setEditThreadId(threadId);
  };

  const handleEditSubmit = async (threadId, title, content) => {
    try {
      setLoading(true);
      await ForumService.editThread(threadId, title, content);
      setEditThreadId(null);
    } catch (error) {
      console.error('Error editing thread:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (threadId) => {
    try {
      setLoading(true);
      await ForumService.deleteThread(threadId);
    } catch (error) {
      console.error('Error deleting thread:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExitEdit = () => {
    setEditThreadId(null);
  };

  const handleAddComment = async (threadId) => {
    try {
      setLoading(true);
      console.log("adding comment");
      await ForumService.addComment(threadId, newComment, currentUserName, currentUser.id);
      console.log("comment added");
      setNewComment('');
    } catch (error) {
      console.error('Error adding comment:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteComment = async (threadId, commentId) => {
    try {
      setLoading(true);
      await ForumService.deleteComment(threadId, commentId);
    } catch (error) {
      console.error('Error deleting comment:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Threads</h2>
      {threads.map(thread => (
        <div key={thread.id}>
          {editThreadId === thread.id ? (
            <EditThreadForm
              initialTitle={thread.title}
              initialContent={thread.content}
              onSubmit={(title, content) => handleEditSubmit(thread.id, title, content)}
              onExit={handleExitEdit}
            />
          ) : (
            <Card title={thread.title} >
              <p>{thread.content}</p>
              <p>Last Updated on {(new Date(thread.createdAt.seconds * 1000 + thread.createdAt.nanoseconds / 1000000)).toLocaleString()}</p>
              <p>Author: {thread.author}</p>
              {thread.alumni && (<p>Alumnus of Digital Coach</p>)}
              {currentUser.id === thread.authorID && (
                <>
                  <Button
                    variant='contained'
                    sx={{ maxWidth: '30%', backgroundColor: '#023047' }}
                    onClick={() => handleEdit(thread.id)}>
                    Edit
                  </Button>
                  <br />
                  <Button
                    variant='contained'
                    sx={{ maxWidth: '30%', backgroundColor: '#023047' }}
                    onClick={() => handleDelete(thread.id)}>
                    Delete
                  </Button>
                </>
              )}
              <br />
              <br />
              <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <form onSubmit={(e) => {
                e.preventDefault(); // Prevent default form submission
                handleAddComment(thread.id); // Call handleAddComment with thread id
              }}>
                <TextField
                  type='text'
                  label='Add a comment'
                  value={newComment}
                  required
                  inputProps={{ minLength: 1,
                    maxLength: 1000,
                  }}
                   style={{ flex: 3 }} 
                  onChange={(e) => setNewComment(e.target.value)}
                />
                <Button
                  variant='contained'
                  type='submit'
                  sx={{ maxWidth: '30%', backgroundColor: '#023047' }}>
                  Add Comment
                </Button>
              </form>
                </div>
              {/* Render comments */}
              {thread.comments && thread.comments.length > 0 && (<h3>Comments:</h3>)}
              {thread.comments && thread.comments.map(comment => (
                <div key={comment.id}>
                  <p>{comment.content}</p>
                  <p>Author: {comment.author}</p>
                  {currentUser.id === comment.authorID && (
                    <Button onClick={() => handleDeleteComment(thread.id, comment.id)}>
                      Delete
                    </Button>
                  )}
                </div>
              ))}
            </Card>
          )}
        </div>
      ))}
    </div>
  );
}

export default ThreadList;

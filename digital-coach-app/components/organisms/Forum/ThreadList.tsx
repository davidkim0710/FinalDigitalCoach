import React, { useState } from 'react';
import Card from '@App/components/atoms/Card';
import ForumService from './forumapi'; // Import ForumService
import { Button } from '@mui/material';
import EditThreadForm from './EditThreadForm'; // Import EditThreadForm
import useAuthContext from '@App/lib/auth/AuthContext';

function ThreadList({ threads, setLoading}) {
  const [editThreadId, setEditThreadId] = useState(null);
  const { currentUser } = useAuthContext();
  const [newComment, setNewComment] = useState('');
  let currentUserName = currentUser._document.data.value.mapValue.fields.name.stringValue;

  const handleEdit = (threadId) => {
    // Set the thread to be edited
    setEditThreadId(threadId);
  };

  const handleEditSubmit = async (threadId, title, content) => {
    try {
      setLoading(true);
      await ForumService.editThread(threadId, title, content);
      // Reset the editThread state to exit the edit mode
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
      setLoading(true);
    } catch (error) {
      console.error('Error deleting thread:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExitEdit = () => {
    setEditThreadId(null); // Function to exit edit mode
  };

  const handleAddComment = async (threadId) => {
    //console.log(event);
    //event.preventDefault();
    try {
      setLoading(true);
      console.log("calling addComment");
      console.log(newComment);
      await ForumService.addComment(threadId, newComment, currentUserName, currentUser.id);
      setNewComment('');
      console.log("finished addComment");
      setLoading(false);
    } catch (error) {
      console.error('Error adding comment:', error);
      setLoading(false);
    }
  };

  const handleDeleteComment = async (threadId, commentId) => {
    try {
      setLoading(true);
      await ForumService.deleteComment(threadId, commentId);
      setLoading(false);
    } catch (error) {
      console.error('Error deleting comment:', error);
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Threads</h2>
      {threads.map(thread => (
        <div key={thread.id}>
          {editThreadId === thread.id ? (
            // Render EditThreadForm if editThread state matches the current thread
            <EditThreadForm
              initialTitle={thread.title}
              initialContent={thread.content}
              onSubmit={(title, content) => handleEditSubmit(thread.id, title, content)}
              onExit={handleExitEdit} // Pass the function to exit edit mode
            />
          ) : (
            // Render thread details with edit and delete buttons if current user matches author
            <Card title={thread.title}>
              <p>{thread.content}</p>
              <p>Last Updated on {(new Date(thread.createdAt.seconds * 1000 + thread.createdAt.nanoseconds / 1000000)).toLocaleString()}</p>
              <p>Author: {thread.author}</p>
              {thread.alumni && (<p>Alumnus of Digital Coach</p>)}
              {/* Conditionally render edit and delete buttons */}
              {currentUser.id === thread.authorID && (
                <>
                  <Button
                    variant='contained'
                    type='submit'
                    sx={{ maxWidth: '30%', backgroundColor: '#023047' }}
                    onClick={() => handleEdit(thread.id)}>
                    Edit
                  </Button>
                  <br />
                  <Button
                    variant='contained'
                    type='submit'
                    sx={{ maxWidth: '30%', backgroundColor: '#023047' }}
                    onClick={() => handleDelete(thread.id)}>
                    Delete
                  </Button>
                </>
              )}
               <form onSubmit={() => handleAddComment(thread.id)}>
                <input
                  type="text"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="Add a comment"
                />
                <Button
                    variant='contained'
                    type='submit'
                    sx={{ maxWidth: '30%', backgroundColor: '#023047' }}>
                    Add Comment
                  </Button>
              </form>
              <p>{thread.comments}</p>
              {thread.comments && thread.comments.map(comment => (
                <div key={comment.id}>
                  <p>{comment.content}</p>
                  <p>Author: {comment.author}</p>
                  {/* Optionally, add delete button for comments */}
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

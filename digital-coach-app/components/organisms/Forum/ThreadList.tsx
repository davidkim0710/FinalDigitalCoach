import React, { useState } from 'react';
import ForumService from './forumapi'; // Import ForumService
import Button from '@App/components/atoms/Button';
import EditThreadForm from './EditThreadForm'; // Import EditThreadForm

function ThreadList({ threads, setLoading }) {
  const [editThread, setEditThread] = useState(null);

  const handleEdit = (threadId) => {
    // Set the thread to be edited
    setEditThread(threadId);
  };

  const handleEditSubmit = async (title, content) => {
    try {
      setLoading(true);
      await ForumService.editThread(editThread, title, content);
      // Reset the editThread state to exit the edit mode
      setEditThread(null);
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

  return (
    <div>
      <h2>Threads</h2>
      {threads.map(thread => (
        <div key={thread.id}>
          {editThread === thread.id ? (
            // Render EditThreadForm if editThread state matches the current thread
            <EditThreadForm
              initialTitle={thread.title}
              initialContent={thread.content}
              onSubmit={(title, content) => handleEditSubmit(title, content)}
            />
          ) : (
            // Render thread details with edit and delete buttons
            <>
              <h3>{thread.title}</h3>
              <p>{thread.content}</p>
              <Button onClick={() => handleEdit(thread.id)}>Edit</Button>
              <Button onClick={() => handleDelete(thread.id)}>Delete</Button>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

export default ThreadList;

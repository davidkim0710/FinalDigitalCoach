import React from 'react';
import ForumService from './forumapi'; // Import ForumService
import Button from '@App/components/atoms/Button';

function ThreadList({ threads, setLoading }) {
  const handleEdit = async (threadId) => {
    const newData = {
      // Provide updated data for the thread
    };
    try {
      await ForumService.editThread(threadId, newData);
    } catch (error) {
      console.error('Error editing thread:', error);
    }
  };

  const handleDelete = async (threadId) => {
    try {
      setLoading(true);
      await ForumService.deleteThread(threadId);
    } catch (error) {
      console.error('Error deleting thread:', error);
    }
  };

  return (
    <div>
      <h2>Threads</h2>
      {threads.map(thread => (
        <div key={thread.id}>
          <h3>{thread.title}</h3>
          <p>{thread.content}</p>
          <Button onClick={() => handleEdit(thread.id)}>Edit</Button>
          <Button onClick={() => handleDelete(thread.id)}>Delete</Button>
        </div>
      ))}
    </div>
  );
}

export default ThreadList;

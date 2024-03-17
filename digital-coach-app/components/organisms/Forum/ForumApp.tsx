import React, { useState, useEffect } from 'react';
import ThreadList from './ThreadList';
import {
  Button
} from '@mui/material';
import ForumService from './forumapi'; // Import ForumService
import NewThreadForm from './NewThreadForm';
import { useAuth } from '@App/lib/auth/AuthContext'; // Import the authentication context

function ForumApp() {
  const [threads, setThreads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false); // State to control form visibility
  const { currentUser } = useAuth(); // Get the current user from the authentication context

  useEffect(() => {
    const fetchThreads = async () => {
      try {
        const threadsData = await ForumService.getAllThreads();
        const threadsArray = threadsData.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        setThreads(threadsArray);
      } catch (error) {
        console.error('Error fetching threads:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchThreads();
  }, [loading]);

  const handleNewThread = async (title, content) => {
    try {
      setLoading(true);
      setIsFormOpen(false); // Close the form after submitting
      // Pass the current user's information when creating a new thread
      await ForumService.createThread(currentUser, title, content);
    } catch (error) {
      console.error('Error creating or fetching threads:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Discussion Forum</h1>
      {isFormOpen ? (
        <NewThreadForm onSubmit={handleNewThread} onClose={() => setIsFormOpen(false)} />
      ) : (
        <Button
          variant='contained'
          type='submit'
          sx={{ maxWidth: '30%', backgroundColor: '#023047' }}
          onClick={() => setIsFormOpen(true)}>
          Create New Thread
        </Button>
      )}
      {loading ? (
        <p>Loading threads...</p>
      ) : (
        <ThreadList threads={threads} setLoading={setLoading} currentUser={currentUser} />
      )}
    </div>
  );
}

export default ForumApp;

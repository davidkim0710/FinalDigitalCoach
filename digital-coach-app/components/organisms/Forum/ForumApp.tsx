import React, { useState, useEffect } from 'react';
import ThreadList from './ThreadList';
import {
  Button,
  TextField
} from '@mui/material';
import ForumService from './forumapi'; // Import ForumService
import NewThreadForm from './NewThreadForm';

function ForumApp() {
  const [threads, setThreads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false); // State to control form visibility
  const [searchQuery, setSearchQuery] = useState(''); // State to hold the search query

  useEffect(() => {
    const fetchThreads = async () => {
      try {
        const threadsData = await ForumService.getAllThreads();
        const threadsArray = await threadsData.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        setThreads(threadsArray);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching threads:', error);
      }
    };

    fetchThreads();
  }, [loading]); 

  const handleNewThread = async (title, content) => {
    try {
      setLoading(true);
      setIsFormOpen(false); // Close the form after submitting
      await ForumService.createThread(title, content);
    } catch (error) {
      console.error('Error creating or fetching threads:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };


  const filteredThreads = threads.filter(thread =>
    thread.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    thread.content.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div>
       <TextField
            type='text'
            label='Search for a Thread '
            value={searchQuery}
            required
            inputProps={{
              maxLength: 50,
            }}
            onChange={handleSearchChange}
      />
      <br />
      <br />
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
      {loading ? ( // Check if either loading or deletingThread is true
        <p>Loading threads...</p>
      ) : (
        <ThreadList threads={filteredThreads} setLoading={setLoading} />
      )}
    </div>
  );
}

export default ForumApp;

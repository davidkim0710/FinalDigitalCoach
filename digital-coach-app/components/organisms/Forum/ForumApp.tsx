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
  const [loading2, setLoading2] = useState(false);
  const [isFormOpen, setIsFormOpen] = useState(false); // State to control form visibility
  const [searchQuery, setSearchQuery] = useState(''); // State to hold the search query

  useEffect(() => {
    const fetchThreads = async () => {
      try {
        const threadsData = await ForumService.getAllThreads();
        const threadsArray = await threadsData.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        setThreads(threadsArray);
        console.log(threads);
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
      setLoading(true);
    }
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  // Filter threads based on the search query
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
      {loading || loading2 ? (
        <p>Loading threads...</p>
      ) : (
        <ThreadList threads={filteredThreads} setLoading={setLoading} setLoading2={setLoading2} />
      )}
    </div>
  );
}

export default ForumApp;

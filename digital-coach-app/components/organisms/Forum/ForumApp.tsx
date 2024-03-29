import React, { useState, useEffect } from 'react';
import ThreadList from './ThreadList';
import {
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import ForumService from './forumapi'; // Import ForumService
import NewThreadForm from './NewThreadForm';
import useAuthContext from '@App/lib/auth/AuthContext';

function ForumApp() {
  const [threads, setThreads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false); // State to control form visibility
  const [searchQuery, setSearchQuery] = useState(''); // State to hold the search query
  const [sortBy, setSortBy] = useState(''); // State to hold the selected sorting option
  const {currentUser} = useAuthContext();
  let currentUserName = currentUser._document.data.value.mapValue.fields.name.stringValue;
  let currUserID = currentUser!.id;

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

  const handleNewThread = async (title, content, isAlumni) => {
    try {
      setLoading(true);
      setIsFormOpen(false); // Close the form after submitting
      await ForumService.createThread(title, content, currentUserName, currUserID, isAlumni);
    } catch (error) {
      console.error('Error creating or fetching threads:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSortChange = (event) => {
    setSortBy(event.target.value);
  };


  const filteredThreads = threads.filter(thread =>
    thread.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    thread.content.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (sortBy === 'alumni') {
    filteredThreads = filteredThreads.filter(thread => thread.alumni);
  } else if (sortBy === 'date-asc') {
    filteredThreads.sort((a, b) => {
      const dateA = new Date(a.createdAt.seconds * 1000);
      const dateB = new Date(b.createdAt.seconds * 1000);
      return dateA - dateB;
    });
  } else if (sortBy === "date-des"){
    filteredThreads.sort((a, b) => {
      const dateA = new Date(a.createdAt.seconds * 1000);
      const dateB = new Date(b.createdAt.seconds * 1000);
      return dateB - dateA;
    });
  }

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
      <div style={{display: 'flex', justifyContent: 'flex-end'}}>
        <FormControl style={{size: "30%" }}>
            <InputLabel>Sort By</InputLabel>
            <Select value={sortBy} onChange={handleSortChange}>
              <MenuItem value="">None</MenuItem>
              <MenuItem value="alumni">Digital Coach Alumni</MenuItem>
              <MenuItem value="date-asc">Date (ascending)</MenuItem>
              <MenuItem value="date-des">Date (descending)</MenuItem>
            </Select>
          </FormControl>
        </div>
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

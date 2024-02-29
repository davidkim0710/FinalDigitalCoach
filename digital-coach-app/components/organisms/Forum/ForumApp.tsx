import React, { useState, useEffect } from 'react';
import ThreadList from './ThreadList';
import NewThreadForm from './NewThreadForm';
import ForumService from './forumapi'; 

function ForumApp() {
  const [threads, setThreads] = useState([]);

  useEffect(() => {
    // Fetch threads when component mounts
    ForumService.getAllThreads().then(threadsData => {
      const threadsArray = threadsData.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      setThreads(threadsArray);
    }).catch(error => {
      console.error('Error fetching threads:', error);
    });
  }, []);

  const handleNewThread = (title, content) => {
    ForumService.createThread(title, content).then(() => {
      // After creating a new thread, fetch all threads again to update the list
      ForumService.getAllThreads().then(threadsData => {
        const threadsArray = threadsData.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        setThreads(threadsArray);
      }).catch(error => {
        console.error('Error fetching threads after creating new thread:', error);
      });
    }).catch(error => {
      console.error('Error creating thread:', error);
    });
  };

  return (
    <div>
      <h1>Discussion Forum</h1>
      <NewThreadForm onSubmit={handleNewThread} />
      <ThreadList threads={threads} />
    </div>
  );
}

export default ForumApp;

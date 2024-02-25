import React, { useState, useEffect } from 'react';
import ThreadList from './ThreadList';
import NewThreadForm from './NewThreadForm';
import { getThreads, createThread } from './forumapi'; // Functions for fetching data from backend

function ForumApp() {
  const [threads, setThreads] = useState([]);

  useEffect(() => {
    // Fetch threads when component mounts
    getThreads().then(threadsData => setThreads(threadsData));
  }, []);

  const handleNewThread = (title, content) => {
    createThread(title, content).then(newThread => {
      setThreads([...threads, newThread]);
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

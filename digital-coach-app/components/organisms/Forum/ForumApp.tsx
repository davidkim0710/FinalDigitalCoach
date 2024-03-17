import React, { useState, useEffect } from 'react';
import ThreadList from './ThreadList';
import ForumService from './forumapi'; // Import ForumService
import NewThreadForm from './NewThreadForm';

function ForumApp() {
  const [threads, setThreads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false); // State to control form visibility

  useEffect(() => {
    const fetchThreads = async () => {
      try {
        const threadsData = await ForumService.getAllThreads();
        const threadsArray = await threadsData.docs.map(doc => ({ id: doc.id, ...doc.data() }));
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
      await ForumService.createThread(title, content);
    } catch (error) {
      console.error('Error creating or fetching threads:', error);
    } finally {
      setLoading(true);
    }
  };

  return (
    <div>
      <h1>Discussion Forum</h1>
      {isFormOpen ? (
        <NewThreadForm onSubmit={handleNewThread} onClose={() => setIsFormOpen(false)} />
      ) : (
        <button onClick={() => setIsFormOpen(true)}>Create New Thread</button>
      )}
      {loading ? (
        <p>Loading threads...</p>
      ) : (
        <ThreadList threads={threads} setLoading={setLoading} />
      )}
    </div>
  );
}

export default ForumApp;

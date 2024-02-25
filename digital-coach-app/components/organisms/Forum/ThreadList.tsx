import React from 'react';

function ThreadList({ threads }) {
  return (
    <div>
      <h2>Threads</h2>
      {threads.map(thread => (
        <div key={thread.id}>
          <h3>{thread.title}</h3>
          <p>{thread.content}</p>
        </div>
      ))}
    </div>
  );
}

export default ThreadList;

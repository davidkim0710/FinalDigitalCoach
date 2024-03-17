import React, { useState } from 'react';
import Card from '@App/components/atoms/Card';
import Button from '../../atoms/Button';

function NewThreadForm({ onSubmit }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(title, content);
    setTitle('');
    setContent('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <Card title = "Create New Thread>
        <div>
          <label>Title:</label>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label>Content:</label>
          <textarea value={content} onChange={(e) => setContent(e.target.value)} required />
        </div>
        <Button onClick = {handleSubmit} >Submit</Button>
      </Card>
    </form>
  );
}

export default NewThreadForm;

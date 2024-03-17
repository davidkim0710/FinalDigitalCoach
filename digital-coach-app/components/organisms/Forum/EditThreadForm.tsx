import React, { useState } from 'react';
import {
  TextField,
  FormControl,
  Button
} from '@mui/material';
import Card from '@App/components/atoms/Card';

function EditThreadForm({ initialTitle, initialContent, onSubmit }) {
  const [title, setTitle] = useState(initialTitle);
  const [content, setContent] = useState(initialContent);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(title, content);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Card title = "Edit Thread">
        <div>
          <label>Title:</label>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label>Content:</label>
          <textarea value={content} onChange={(e) => setContent(e.target.value)} required />
        </div>
        <Button type="submit">Submit</Button>
      </Card>
    </form>
  );
}

export default EditThreadForm;

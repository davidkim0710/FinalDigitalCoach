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
        <FormControl fullWidth>
          <TextField
            type='text'
            label='Title '
            value={title}
            required
            onChange={(e) => setTitle(e.target.value)}
          />
          <br />
          <TextField
            type='text'
            label='Thread Content '
            value={content}
            required
            onChange={(e) => setContent(e.target.value)}
          />
          <br />
        <div>
          <label>Title:</label>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label>Content:</label>
          <textarea value={content} onChange={(e) => setContent(e.target.value)} required />
        </div>
        <Button
            variant='contained'
            type='submit'
            sx={{ maxWidth: '30%', backgroundColor: '#023047' }}
            onClick = {handleSubmit}>
            Submit
          </Button>
          </FormControl>
      </Card>
    </form>
  );
}

export default EditThreadForm;

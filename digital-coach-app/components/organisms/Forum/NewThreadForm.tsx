import React, { useState } from 'react';
import Card from '@App/components/atoms/Card';
import {
  TextField,
  FormControl,
  Button
} from '@mui/material';

function NewThreadForm({ onSubmit, onClose }) {
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
      <Card title="Create New Thread">
        <FormControl fullWidth>
          <TextField
            type='text'
            label='Title'
            value={title}
            required
            onChange={(e) => setTitle(e.target.value)}
          />
          <br />
          <TextField
            type='text'
            label='Thread Content'
            value={content}
            required
            onChange={(e) => setContent(e.target.value)}
          />
          <br />
          <Button
            variant='contained'
            type='submit'
            sx={{ marginRight: '10px', backgroundColor: '#023047' }}
          >
            Submit
          </Button>
          <br />
          <Button
            variant='contained'
            color='error'
            sx={{ marginRight: '10px' }}
            onClick={onClose}
          >
            Exit
          </Button>
        </FormControl>
      </Card>
    </form>
  );
}

export default NewThreadForm;

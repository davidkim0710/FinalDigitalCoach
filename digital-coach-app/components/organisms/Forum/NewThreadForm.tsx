import React, { useState } from 'react';
import Card from '@App/components/atoms/Card';
import {
  TextField,
  FormControl,
  Button,
  FormControlLabel,
  Checkbox,
} from '@mui/material';

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
      <Card title = "Create New Thread">
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
        <Button
          variant='contained'
          type='submit'
          sx={{ maxWidth: '30%', backgroundColor: '#023047' }}
          onClick = {handleSubmit}>
          Submit
        </Button>
      </Card>
    </form>
  );
}

export default NewThreadForm;

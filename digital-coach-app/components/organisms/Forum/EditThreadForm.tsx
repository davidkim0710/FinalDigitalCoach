import React, { useState } from 'react';
import {
  TextField,
  FormControl,
  Button
} from '@mui/material';
import Card from '@App/components/atoms/Card';

function EditThreadForm({ initialTitle, initialContent, onSubmit, onExit }) {
  const [title, setTitle] = useState(initialTitle);
  const [content, setContent] = useState(initialContent);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(title, content);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Card title="Edit Thread">
        <FormControl fullWidth>
          <TextField
            type='text'
            label='Title'
            value={title}
            required
            inputProps={{ minLength: 1,
              maxLength: 40,
            }}
            onChange={(e) => setTitle(e.target.value)}
          />
          <br />
          <TextField
            type='text'
            label='Thread Content'
            value={content}
            required
            inputProps={{ minLength: 1,
              maxLength: 1000,
            }}
            onChange={(e) => setContent(e.target.value)}
          />
          <div style={{ display: 'flex', justifyContent: 'center' }}>
          <br />
          <Button
            variant='contained'
            type='submit'
            sx={{ marginRight: '1000px', backgroundColor: '#023047' }}
          >
            Submit
          </Button>
          <Button
            variant='contained'
            color='error'
            onClick={onExit} // Call onClose function when the button is clicked
          >
            Exit
          </Button>
            </div>
        </FormControl>
      </Card>
    </form>
  );
}

export default EditThreadForm;

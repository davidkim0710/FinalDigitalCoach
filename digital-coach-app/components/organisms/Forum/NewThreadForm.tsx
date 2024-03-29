import React, { useState } from 'react';
import { Button, Checkbox, FormControl,FormControlLabel, TextField } from '@mui/material';
import Card from '@App/components/atoms/Card';

function NewThreadForm({ onSubmit, onClose }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isAlumni, setIsAlumni] = useState(false); // State for checkbox

  const handleSubmit = (event) => {
    event.preventDefault();
    // Call onSubmit with form data
    onSubmit(title, content, isAlumni);
    // Reset form fields
    setTitle('');
    setContent('');
    setIsAlumni(false);
    // Close the form
    onClose();
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
            rows={4}
          />
          <br />
          <FormControlLabel
            control={
              <Checkbox
                checked={isAlumni}
                onChange={(event) => setIsAlumni(event.target.checked)}
                color="primary"
              />
            }
            label="Are you a Digital Coach alumni (practiced at least 1 interview)?"
          />
          <br />
          <br />
          <Button variant="contained" type="submit">
            Submit
          </Button>
          </FormControl>
        </Card>
    </form>
  );
}

export default NewThreadForm;

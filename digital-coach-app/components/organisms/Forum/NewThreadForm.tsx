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
          <div style={{ display: 'flex', justifyContent: 'center' }}>
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
            onClick={onClose} // Call onClose function when the button is clicked
          >
            Exit
          </Button>
            </div>
          </FormControl>
        </Card>
    </form>
  );
}

export default NewThreadForm;

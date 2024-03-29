import React, { useState } from 'react';
import { Button, Checkbox, FormControlLabel, TextField } from '@mui/material';
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
      <TextField
        label="Title"
        value={title}
        onChange={(event) => setTitle(event.target.value)}
        required
        fullWidth
      />
      <br />
      <br />
      <TextField
        label="Content"
        value={content}
        onChange={(event) => setContent(event.target.value)}
        required
        fullWidth
        multiline
        rows={4}
      />
      <br />
      <br />
      {/* Checkbox for "Are you a Digital Coach alumni (practiced at least one interview)?" */}
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
        </Card>
    </form>
  );
}

export default NewThreadForm;

import React, { useState } from 'react';
import { Button, Checkbox, FormControlLabel, TextField } from '@mui/material';

function NewThreadForm({ onSubmit, onClose }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [didCoachHelp, setDidCoachHelp] = useState(false); // State for checkbox

  const handleSubmit = (event) => {
    event.preventDefault();
    // Call onSubmit with form data
    onSubmit(title, content, didCoachHelp);
    // Reset form fields
    setTitle('');
    setContent('');
    setDidCoachHelp(false);
    // Close the form
    onClose();
  };

  return (
    <form onSubmit={handleSubmit}>
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
      {/* Checkbox for "Did Digital Coach help you land a job" */}
      <FormControlLabel
        control={
          <Checkbox
            checked={didCoachHelp}
            onChange={(event) => setDidCoachHelp(event.target.checked)}
            color="primary"
          />
        }
        label="Did Digital Coach help you land a job?"
      />
      <br />
      <br />
      <Button variant="contained" type="submit">
        Submit
      </Button>
    </form>
  );
}

export default NewThreadForm;

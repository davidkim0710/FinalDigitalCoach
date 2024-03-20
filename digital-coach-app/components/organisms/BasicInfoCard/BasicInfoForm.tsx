import { useState } from 'react';
import {
  TextField,
  FormControl,
  Button,
  FormControlLabel,
  Checkbox,
} from '@mui/material';
import { useForm } from 'react-hook-form';
import InterviewSetsService from '@App/lib/interviewSets/interviewSetsService';
import QuestionSetsService from '@App/lib/questionSets/QuestionSetsService';

interface userInfo {
  userId: string;
}

export default function BasicInfoForm({ userId }: userInfo) {
  const {} = useForm();
  const [questionSetName, setQuestionSetName] = useState('');
  const [timePerQ, setTimePerQ] = useState('');
  const [numRetries, setNumRetries] = useState('');
  const [makeInterview, setMakeInterview] = useState(false);

  /**
   * This function will be called when the form is submitted.
   * On submission, it will create a question set with the set interview name
   * with the other parameters being left blank.
   * This will also create an inteview set with the given Interview Name and
   * the user inputted time per question and number of retries
   * @returns The created question set
   */
  const createInterviewSet = async (e: { preventDefault: () => void }) => {
    e.preventDefault();
    console.log(`${questionSetName}, ${timePerQ}, ${numRetries}`);
    //Create interview set first
    //Now create question set
    const questionSet = {
      title: questionSetName,
      description: '',
      questions: [],
      isFeatured: false,
      createdBy: userId,
    };
    const thisQuestionSet = QuestionSetsService.createQuestionSet(
      questionSet
    );
    // A reference to the questionSet is stored in the newly created interviewSet
    if (makeInterview) {
      const interviewSet = {
        name: questionSetName,
        minutesToAnswer: parseInt(timePerQ),
        numberOfRetries: parseInt(numRetries),
        questionSetRef: thisQuestionSet.id,
      };
      console.log('Calling create function in BasicInfoForm');
      InterviewSetsService.create(userId, interviewSet);
    }
    location.reload();
  };

  return (
    <form onSubmit={createInterviewSet}>
      <FormControl fullWidth>
        <TextField
          type='text'
          label='Question Set Name'
          placeholder='Give the question set a fitting name'
          required
          onChange={(e) => setQuestionSetName(e.target.value)}
        />
        <br />
        <TextField
          type='number'
          label='Minutes Given to Answer'
          placeholder='How long do you have per question?'
          defaultValue=''
          helperText='Leave blank for no time limit'
          onChange={(e) => setTimePerQ(e.target.value)}
        />
        <br />
        <TextField
          type='number'
          label='Number of Retries Per Question'
          placeholder='How many times can you retry the question?'
          defaultValue=''
          helperText='Leave blank for no limit on retries'
          onChange={(e) => setNumRetries(e.target.value)}
        />
        <br />
        <div>
          <FormControlLabel
            control={
              <Checkbox
                checked={makeInterview}
                onChange={() => {
                  setMakeInterview(!makeInterview);
                }}
                sx={{ paddingLeft: '25px' }}
              />
            }
            label='Create Interview Set with this Question Set'
          />
          <Button
            variant='contained'
            type='submit'
            sx={{ maxWidth: '30%', backgroundColor: '#023047' }}>
            Create Question Set
          </Button>
        </div>
      </FormControl>
    </form>
  );
}

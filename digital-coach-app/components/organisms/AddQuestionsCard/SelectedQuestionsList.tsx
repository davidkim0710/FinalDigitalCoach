import React, { useState, useEffect } from 'react';
import useAuthContext from '@App/lib/auth/AuthContext';
import { MenuItem, Select, InputLabel } from '@mui/material';
import QuestionService from '@App/lib/question/QuestionService';
import styles from './AddQuestionsCard.module.scss';
import QuestionSetsService from '@App/lib/questionSets/QuestionSetsService';

interface propsInfo {
  selectedSet: { questions: any[]; title: string; id: string };
  setSelectedSet: (set: {
    questions: any[];
    title: string;
    id: string;
  }) => void;
}

const sampleSubjects = [
  'Business Accounting and Analytics',
  'Business Management',
  'Business Marketing',
  'Business Operations',
  'Business Strategy',
  'Business Technology',
  'Data Science',
  'Finance',
  'Human Resources',
  'Information Technology',
  'Law',
];

export default function SelectedQuestionsList(props: propsInfo) {
  const { currentUser } = useAuthContext();
  const [userQuestionSets, setUserQuestionSets] = useState<any[]>([]);
  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    async function fetchUserQuestionSets() {
      const userQuestionsSets: any[] = (
        await QuestionSetsService.getQuestionSetByUserId(currentUser!.id)
      ).docs.map((doc) => {
        return { id: doc.id, ...doc.data() };
      });
      setUserQuestionSets(userQuestionsSets);
    }
    fetchUserQuestionSets();
  }, []);

  useEffect(() => {
    // Fires when a question set is selected, need to get the corresponding questions and show them
    console.log('selectedSet useEffectFired');
    const fetchQuestions = async () => {
      const selectedQuestions: any[] = [];
      for (let i = 0; i < props.selectedSet.questions.length; i++) {
        selectedQuestions.push(
          await QuestionService.getById(props.selectedSet.questions[i])
        );
      }
      setQuestions(selectedQuestions);
    };
    setLoading(true);
    fetchQuestions();
    setLoading(false);
  }, [props.selectedSet]);

  return (
    <div className={styles.AddQuestionsCard_questionList}>
      <InputLabel id='question-set-select-label'>Question Set</InputLabel>
      <Select
        labelId='question-set-select-label'
        id='question-set-select'
        label='Question Set'
        variant='standard'
        value={props.selectedSet}
        fullWidth
        onChange={(event) => {
          props.setSelectedSet(event.target.value as propsInfo['selectedSet']);
        }}>
        {userQuestionSets.map((questionSet) => (
          <MenuItem key={questionSet.id} value={questionSet}>
            {questionSet.title}
          </MenuItem>
        ))}
      </Select>
      {loading ? (
        <p>Loading...</p>
      ) : questions.length === 0 ? (
        <div>
          <p>No questions in this question set</p>
        </div>
      ) : (
        <div>
          <p>Currently Selected Questions:</p>
          {questions.map((question) => {
            return (
              <p key={question._key.path.segments[1]}>
                {
                  question._document.data.value.mapValue.fields.question
                    .stringValue
                }
              </p>
            );
          })}
        </div>
      )}
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { MenuItem, Select, InputLabel } from '@mui/material';
import QuestionService from '@App/lib/question/QuestionService';
import styles from './AddQuestionsCard.module.scss';
import QuestionSetsService from '@App/lib/questionSets/QuestionSetsService';
import '@App/lib/questionSets/useGetFeaturedQuestionSets.ts';
import useAuthContext from '@App/lib/auth/AuthContext';

interface propsInfo {
  selectedSet: { questions: any[]; title: string; id: string };
  setSelectedSet: (set: {
    questions: any[];
    title: string;
    id: string;
  }) => void;
  questions: any[];
  setQuestions: (arg0: any[]) => void;
  showQuestions: boolean;
  setShowQuestions: (arg0: boolean) => void;
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
  const [userQuestionSets, setUserQuestionSets] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
   const { currentUser } = useAuthContext();

  useEffect(() => {
    async function fetchUserQuestionSets() {
      const userQuestionsSets: any[] = (
        await QuestionSetsService.getQuestionSetByUserId(currentUser!.id)
      ).docs.map((doc) => {
        return { id: doc.id, ...doc.data() };
      });
      setUserQuestionSets(userQuestionsSets);
    }
    console.log(userQuestionSets);
    fetchUserQuestionSets();
  }, []);

  useEffect(() => {
    // Fires when a question set is selected, need to get the corresponding questions and show them
    console.log('selectedSet useEffectFired');
    const fetchQuestions = async () => {
      const selectedQuestions: any[] = [];
      console.log(props.selectedSet.questions.length);
      for (let i = 0; i < props.selectedSet.questions.length; i++) {
        selectedQuestions.push(
          await QuestionService.getById(props.selectedSet.questions[i])
        );
      }
      props.setQuestions(selectedQuestions);
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
          props.setShowQuestions(true);
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
      ) : props.questions.length === 0 || !props.showQuestions ? (
        <div>
          <p>No questions in this question set</p>
        </div>
      ) : (
        <div>
          <p>Questions:</p>
          {props.questions.map((question) => {
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

import React, { useState, useEffect } from 'react';
import Avatar from '@App/components/atoms/Avatar';
import Card from '@App/components/atoms/Card';
import useAuthContext from '@App/lib/auth/AuthContext';
import AuthGuard from '@App/lib/auth/AuthGuard';
import InterviewService from '@App/lib/interview/InterviewService';

import styles from '@App/styles/ProfilePage.module.scss';

import { Tooltip, IconButton } from '@mui/material';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

function ProfilePage() {
  const { currentUser } = useAuthContext();
  const [interviews, setInterviews] = useState<any[]>([]);

  const opennessText = `
	High is a sign of:
	-Curiosity
	-Imagination
	-Creativity
	-Openness to trying new things
	-Unconventionality\n
	Low is a sign of:
	-Predictability
	-Lack of imagination
	-Dislike of change
	-Preferring a routine
	-Preferring what's traditional
	`;

	const conscientiousnessText = `
	High is a sign of:
	-Competence
	-Organization
	-Dutifulness
	-Achievement Striving
	-Self-Discipline
	-Deliberation\n
	Low is a sign of:
	-Incompetence
	-Disorganization
	-Carelessness
	-Procrastination
	-Indiscipline
	-Impulsive
	`

	const extraversionText = `
	High is a sign of:
	-Sociableness
	-Being energized by social situations
	-Seeking excitement
	-Enjoying being the center of attention
	-Being outgoing\n
	Low is a sign of:
	-Preferring solitude
	-Being exhausted by social situations
	-Being reflective
	-Disliking being the center of attention
	-Being reserved
	`

	const agreeablenessText = `
	High is a sign of:
	-Trustingness
	-Straightforwardness
	-Altruism
	-Compliance
	-Modesty
	-Sympathy
	-Empathy\n
	Low is a sign of: 
	-Skepticism
	-Being demanding
	-Likeliness to insult or belittle others
	-Stubbornness
	-Being a show off
	-Unsympathetic
	-Not caring how others feel
	`

	const neuroticismText = `
	-High is a sign of:
	-Anxiousness
	-Irritability
	-Stress
	-Self consciousness
	-Vulnerability
	-Dramatic mood shifts\n
	Low is a sign of:
	-Less worrying
	-Calmness
	-Emotional stability
	-Confidence
	-Resilience
	-Resistance to feeling sadness
	`;




  useEffect(() => {
    const getInterviews = async () => {
      const result = await InterviewService.fetchUserInterviews(
        currentUser!.id
      );
	    console.log(result);
      setInterviews(result.docs.map((doc) => doc.data()));
    };
    getInterviews();
  }, []);

  return (
    <div className={styles.ProfilePage}>
      <h1>Your Profile</h1>

      <div className={styles.ProfilePage_avatarWrapper}>
        {currentUser?.data()?.avatarUrl && (
          <Avatar size={125} src={currentUser?.data()!.avatarUrl} />
        )}
      </div>

      <div className={styles.ProfilePage_body}>
        <div className={styles.ProfilePage_bodyLeft}>
          <Card title='Name'>{currentUser?.data()?.name}</Card>
          <Card title='Email'>{currentUser?.data()?.email}</Card>
        </div>

        <div className={styles.ProfilePage_bodyRight}>
          <Card title='Major'>{currentUser?.data()?.concentration}</Card>
          <Card title='Experience Level'>
            {currentUser?.data()?.proficiency}
          </Card>
          <Card title='Previous Interview Scores'>
			{
				Object.keys(interviews).length !== 0 ? (
					<div>
						{
							interviews.filter((interview) => Object.keys(interview.result).length > 0).map((interview) => { 
								return(
									<Card>
										<p>Interview: {interview.title}</p>
										<p>Time: {new Date(interview.createdAt.seconds * 1000).toString()}</p>
										<p>Aggregate Score (0 to 100): {interview.result.aggregateScore}</p>
										<p>Big Five Scores (-10 to 10): </p>
										<ul>
											<li>
												Openness: {interview.result.bigFive.o} 
												<Tooltip title={
													<span style={{whiteSpace: 'pre-line' }}>{opennessText}</span>
													}>
													<IconButton>
														<HelpOutlineIcon>
														</HelpOutlineIcon>
													</IconButton>
												</Tooltip>
											</li>
											<li>
												Conscientiousness: {interview.result.bigFive.c}
												<Tooltip title={
													<span style={{whiteSpace: 'pre-line' }}>{conscientiousnessText}</span>
													}>
													<IconButton>
														<HelpOutlineIcon>
														</HelpOutlineIcon>
													</IconButton>
												</Tooltip>
											</li>
											<li>Extraversion: {interview.result.bigFive.e}
											<Tooltip title={
													<span style={{whiteSpace: 'pre-line' }}>{extraversionText}</span>
													}>
													<IconButton>
														<HelpOutlineIcon>
														</HelpOutlineIcon>
													</IconButton>
												</Tooltip></li>
											<li>Agreeableness: {interview.result.bigFive.a}
											<Tooltip title={
													<span style={{whiteSpace: 'pre-line' }}>{agreeablenessText}</span>
													}>
													<IconButton>
														<HelpOutlineIcon>
														</HelpOutlineIcon>
													</IconButton>
												</Tooltip></li>
											<li>Neuroticism: {interview.result.bigFive.n}
											<Tooltip title={
													<span style={{whiteSpace: 'pre-line' }}>{neuroticismText}</span>
													}>
													<IconButton>
														<HelpOutlineIcon>
														</HelpOutlineIcon>
													</IconButton>
												</Tooltip></li>
										</ul>
									</Card>
								)
							})
						}
					</div>
				) : (
					<p>No previous interviews found.</p>
				)
			}
          </Card>
        </div>
      </div>
    </div>
  );
}

export default function Profile() {
  return (
    <AuthGuard>
      <ProfilePage />
    </AuthGuard>
  );
}

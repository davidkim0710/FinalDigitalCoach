import { useState } from "react";
import Modal from "react-modal";

Modal.setAppElement("#__next");

interface Props {
  isOpen: boolean;
  handleClose: () => void;
  handleAdd: (questionId: string, questionSetId: string) => Promise<void>;
  modal: string;
  questionSets: any[];
  question: any;
}

import { Card, Box, Select, MenuItem, Button } from "@mui/material";

function AddQuestionToSetModal(props: Props) {
  const [showModal, setShowModal] = useState(props.isOpen);
  const [selectedQuestionSet, setSelectedQuestionSet] = useState(props.questionSets[0].id);

  const handleClose = () => {
    setShowModal(false);
    props.handleClose();
  };

  const handleAdd = () => {
    props.handleAdd(selectedQuestionSet, props.question);
    handleClose();
  };

  return (
    <div>
      <Modal isOpen={showModal} onRequestClose={handleClose} className="addModal">
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
          <Card sx={{ pl: 2, pr: 2, pb: 2 }}>
            <h1>Add Question</h1>
            <Select id="question-set-select" value={selectedQuestionSet} onChange={(e) => setSelectedQuestionSet(e.target.value)}>
              {props.questionSets.map((questionSet) => (
                <MenuItem key={"qSet." + questionSet.id} value={questionSet.id}>
                  {questionSet.title}
                </MenuItem>
              ))}
            </Select>
			<Box sx={{ p:2 }}>
				<Button variant="contained" onClick={handleAdd}>
				Add
				</Button>
				<Button variant="contained" sx={{ backgroundColor: "red" }} onClick={handleClose}>
				Cancel
				</Button>

			</Box>
          </Card>
        </Box>
      </Modal>
    </div>
  );
}

export default AddQuestionToSetModal;

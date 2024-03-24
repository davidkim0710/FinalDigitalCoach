import {
  addDoc,
  collection,
  CollectionReference,
  DocumentReference,
  doc,
  Firestore,
  getDoc,
  getDocs,
  getFirestore,
  query,
  setDoc,
  Timestamp,
  where,
  updateDoc,
  arrayUnion,
} from 'firebase/firestore';
import FirebaseService from '../firebase/FirebaseService';
import { IBaseQuestion } from '../question/models';

interface IQuestionSetAttributes {
  title: string;
  description: string;
  questions: string[];
  isFeatured: boolean;
  createdBy: string | null;
}

interface IQuestionSet extends IQuestionSetAttributes {
  createdAt: Timestamp;
}

class QuestionSetsService extends FirebaseService {
  private firestore: Firestore;

  constructor() {
    super();

    this.firestore = getFirestore(this.app);
  }

  private getCollectionRef() {
    return collection(
      this.firestore,
      'questionSets'
    ) as CollectionReference<IQuestionSet>;
  }

  private getDocRef(qsId: string) {
    return doc(
      this.firestore,
      'questionSets',
      qsId
    ) as DocumentReference<IQuestionSetAttributes>;
  }

  /**
   * This function creates a new question set in the database and returns a promise that resolves to
   * the newly created question set.
   * @param {IQuestionSetAttributes} questionSetAttr - IQuestionSetAttributes
   * @returns A promise that resolves to a document reference.
   */
  async createQuestionSet(questionSetAttr: IQuestionSetAttributes) {
    const collectionRef = this.getCollectionRef();

    const questionSet = {
      ...questionSetAttr,
      createdAt: Timestamp.now(),
    };

    const questionSetRef = await addDoc(collectionRef, questionSet);
    return getDoc(questionSetRef);
  }

  getAllQuestionSets() {
    const collectionRef = this.getCollectionRef();

    return getDocs(collectionRef);
  }

  /**
   * Get all the documents in the collection where the isFeatured field is true.
   * @returns An array of question sets.
   */
  getFeaturedQuestionSets() {
    const collectionRef = this.getCollectionRef();
    const isFeaturedFilter = where('isFeatured', '==', true);
    const q = query(collectionRef, isFeaturedFilter);

    return getDocs(q);
  }

  async updateQuestionSet({
    qsid,
    title,
    description,
    questions = [],
  }: {
    qsid: string;
    title?: string;
    description?: string;
    questions?: string[];
  }) {
    const ref = this.getCollectionRef();

    const foundQuestionSet = (await getDoc(doc(ref, qsid))).data();

    if (!foundQuestionSet) throw new Error('Question set not found');

    await setDoc(
      doc(ref, qsid),
      {
        ...foundQuestionSet,
        title: title || foundQuestionSet.title,
        description: description || foundQuestionSet.description,
        questions: questions || foundQuestionSet.questions,
      },
      { merge: true }
    );
    return await getDoc(doc(ref, qsid));
  }

  async addQuestionToSet(qsid: string, qid: string) {
    console.log(qsid);
    const questionSetRef = this.getCollectionRef();
    console.log(questionSetRef);
    const questionsRef = collection(
      this.firestore,
      'questions'
    ) as CollectionReference<IBaseQuestion>;
    console.log(questionsRef);

    const foundQuestionSet = await getDoc(doc(questionSetRef, qsid));
    console.log(foundQuestionSet)
    console.log(qid)
    try{const foundQuestion = await getDoc(doc(questionsRef, qid));}catch(e){console.log(e)}

    if (!foundQuestionSet)
      throw new Error('Error adding question set: Question set not found!');
    if (!foundQuestion)
      throw new Error('Error adding question set: Question not found!');

    if (foundQuestionSet.data()?.questions.includes(qid))
      throw new Error(
        'Error adding question set: Question already exists in set!'
      );

    await updateDoc(doc(questionSetRef, qsid), {
      questions: arrayUnion(qid),
    });
  }

  async getQuestionSetByUserId(userId: string) {
    const collectionRef = this.getCollectionRef();
    const createdByFilter = where('createdBy', '==', userId);
    const q = query(collectionRef, createdByFilter);

    return await getDocs(q);
  }

  async getQuestionSetById(qsId: string) {
    const qsDocRef = this.getDocRef(qsId);
    try {
      return await getDoc(qsDocRef);
    } catch (e) {
      throw e;
    }
  }

  async getQuestionSetByName(qsName: string) {
    const qsCollection = this.getCollectionRef();
    const thisQsFilter = where('title', '==', qsName);
    const qs = query(qsCollection, thisQsFilter);

    return await getDocs(qs);
  }
}

export default new QuestionSetsService();

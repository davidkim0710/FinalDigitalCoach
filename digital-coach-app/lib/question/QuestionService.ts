import FirebaseService from "@App/lib/firebase/FirebaseService";
import {
  addDoc,
  collection,
  CollectionReference,
  Firestore,
  getDocs,
  getFirestore,
  query,
  QueryDocumentSnapshot,
  Timestamp,
  where,
  orderBy,
  doc,
  getDoc,
  deleteDoc,
  updateDoc,
  arrayUnion,
  startAt,
  startAfter,
  limit,
  endBefore,
  DocumentReference,
} from "firebase/firestore";
import { IBaseQuestion, IBaseQuestionAttributes, IQuestion, TQuestionType, TSubject, TExperienceLevel } from "@App/lib/question/models";

class QuestionService extends FirebaseService {
  private firestore: Firestore;

  constructor() {
    super();
    this.firestore = getFirestore(this.app);
  }

  private getCollectionRef() {
    return collection(this.firestore, "questions") as CollectionReference<IBaseQuestion>;
  }

  private getDocRef(qId: string) {
    return doc(this.firestore, "questions", qId) as DocumentReference<IBaseQuestionAttributes>;
  }

  private docToModel(doc: QueryDocumentSnapshot<IBaseQuestion>): IQuestion {
    return {
      gid: doc.id,
      ...(doc.data() as IBaseQuestion),
    };
  }

  /**
   * This function takes a base question object, adds a timestamp to it, and then adds it to the
   * database.
   * @param {IBaseQuestionAttributes} baseQuestion - IBaseQuestionAttributes
   * @returns A promise that resolves to the document ID of the newly created document.
   */
  async addQuestion(baseQuestion: IBaseQuestionAttributes) {
    const question: IBaseQuestion = {
      ...baseQuestion,
      type: baseQuestion.type || "Any",
      experienceLevel: baseQuestion.experienceLevel || "Any",
      companies: baseQuestion.companies || [],
      popularity: baseQuestion.popularity || 0,
      createdBy: baseQuestion.createdBy || null,
      lastUpdatedAt: Timestamp.now(),
      createdAt: Timestamp.now(),
    };
    return await addDoc(this.getCollectionRef(), question);
  }

  /**
   * This function returns a promise that resolves to an array of objects, each of which represents a
   * question.
   * @returns An array of objects.
   */
  async getAllQuestions() {
    return await getDocs(this.getCollectionRef());
  }

  /**
   * This function returns a promise that resolves to an array of documents that match the given id
   * @param {string} id - string - the position to filter by
   * @returns An array of documents that match the query.
   */
  async getById(id: string) {
    const ref = this.getDocRef(id);
    try {
      return await getDoc(ref);
    } catch (e) {
      throw e;
    }
  }

  /**
   * It returns a promise that resolves to an array of documents that match the given subject
   * @param {TSubject} subject - TSubject - the subject to filter by
   * @returns An array of documents that match the query.
   */
  async getBySubject(subject: TSubject) {
    const ref = this.getCollectionRef();

    const filter = where("subject", "==", subject);

    return await getDocs(query(ref, filter));
  }

  /**
   * This function returns a promise that resolves to an array of documents that match the given position
   * @param {string} position - string - the position to filter by
   * @returns An array of documents that match the query.
   */
  async getByPosition(position: string) {
    const ref = this.getCollectionRef();

    const filter = where("position", "==", position);

    return await getDocs(query(ref, filter));
  }

  /**
   * This function returns a promise that resolves to an array of documents that match the given company
   * @param {Array<string>} companies - Array<string> - the company to filter by
   * @returns An array of documents that match the query.
   */
  async getByCompany(companies: Array<string>) {
    const ref = this.getCollectionRef();

    const filter = where("companies", "array-contains-any", companies);

    return await getDocs(query(ref, filter));
  }

  /**
   * This function returns a promise that resolves to an array of documents that match the given question type
   * @param {string} type - string - the question type to filter by
   * @returns An array of documents that match the query.
   */
  async getByType(type: string) {
    const ref = this.getCollectionRef();

    const filter = where("type", "==", type);

    return await getDocs(query(ref, filter));
  }

  /**
   * This function returns a promise that resolves to an array of question documents
   * sorted by popularity, descending.
   * @returns An array of documents that match the query.
   */
  async getByPopularityDesc() {
    const ref = this.getCollectionRef();

    const filter = orderBy("popularity", "desc");

    return await getDocs(query(ref, filter));
  }

  /**
   *
   *
   * @param {string} qid - string - the question ID
   * @param {TSubject} subject - TSubject - the new subject
   * @param {string} question - string - the new question text
   * @param {TQuestionType} type - TQuestionType - the new question type
   * @param {string} position - string - the new job position
   * @param {Array<string>} companies - Array<string> - the new companies
   * @param {number} popularity - number - the new popularitye
   * @returns
   */
  async updateQuestion({
    qid,
    subject,
    question,
    type,
    experienceLevel,
    companies = [],
    popularity,
  }: {
    qid: string;
    subject?: TSubject;
    question?: string;
    type?: TQuestionType;
    experienceLevel?: TExperienceLevel;
    companies?: Array<string>;
    popularity?: number;
  }) {
    const ref = this.getCollectionRef();

    const foundQuestion = (await getDoc(doc(ref, qid))).data();

    if (!foundQuestion) throw new Error("Question not found!");

    // Note: This returns undefined; it does not return the updated document.
    await updateDoc(doc(ref, qid), {
      ...foundQuestion,
      subject: subject || foundQuestion.subject,
      question: question || foundQuestion.question,
      type: type || foundQuestion.type,
      experienceLevel: experienceLevel || foundQuestion.experienceLevel,
      companies: companies || foundQuestion.companies,
      popularity: popularity || foundQuestion.popularity || 0,
      lastUpdatedAt: Timestamp.now(),
    });

    return await getDoc(doc(ref, qid)); // This returns the updated document.
  }

  /**
   * This function deletes a question from the database.
   * @param {string} qid - string - the question ID
   * @returns A promise that resolves to the deleted question.
   **/
  async deleteQuestion(qid: string) {
    const ref = this.getCollectionRef();

    const foundQuestion = await getDoc(doc(ref, qid));

    if (!foundQuestion) throw new Error("Error deleting question: Question not found!");

    await deleteDoc(doc(ref, qid));

    return foundQuestion;
  }

  /**
   * This function adds companies to a question.
   * @param {string} qid - string - the question ID
   * @param {Array<string>} companies - Array<string> - the companies to add
   * @returns A promise that resolves to the updated question.
   * @todo Re-implement using transactions to reduce the number of database calls.
   */
  async addCompaniesToQuestion(qid: string, companies: string[]) {
    const ref = this.getCollectionRef();

    const foundQuestion = (await getDoc(doc(ref, qid))).data();

    if (!foundQuestion) throw new Error("Error adding company to question: Question not found!");

    if (foundQuestion.companies.some((company) => companies.includes(company))) throw new Error("Error adding company to question: Company already exists!");

    await updateDoc(doc(ref, qid), {
      ...foundQuestion,
      companies: arrayUnion(...companies),
      lastUpdatedAt: Timestamp.now(),
    });

    return await getDoc(doc(ref, qid));
  }

  /**
   *
   * @param {TSubject} subject - The subject to filter by
   * @param {TQuestionType} type - The question type to filter by
   * @param {TExperienceLevel} experience - The experience level to filter by
   * @param {boolean} popularitySort - Determines whether or not to sort by popularity, descending
   * @param {string} searchTerm - The search term to filter by
   * @returns A promise that resolves to an array of documents that match the given filters.
   */
  async getByFilters(subject: TSubject, type: TQuestionType, experience: TExperienceLevel, popularitySort: boolean, searchTerm: string, resultLimit: number, anchorDoc: any) {
    const ref = this.getCollectionRef();
    searchTerm = searchTerm
      .toLowerCase()
      .replace(/\!|\.|\,|\'|\"|\?|\;|\:|\`|\~/g, "")
      .split(" ")
      .join(" ");
    const filters = [
      subject === "Any" ? null : where("subject", "==", subject),
      type === "Any" ? null : where("type", "==", type),
      experience === "Any" ? null : where("experienceLevel", "==", experience),
      popularitySort ? orderBy("popularity", "desc") : (null as any),
      searchTerm ? where("keywords", "array-contains", searchTerm) : null,
      anchorDoc ? startAfter(anchorDoc) : null,
    ].filter((f) => f !== null);
    filters.push(limit(resultLimit));
    console.log(filters)
    let qs = await getDocs(query(ref, ...filters))
    console.log(qs);
    return qs;
  }
}

export default new QuestionService();

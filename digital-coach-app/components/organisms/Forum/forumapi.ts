import {
  addDoc,
  collection,
  deleteDoc,
  DocumentReference,
  Firestore,
  getDocs,
  getFirestore,
  query,
  updateDoc,
} from "firebase/firestore";

class ForumService {
  private firestore: Firestore;

  constructor() {
    this.firestore = getFirestore();
  }

  private getThreadsCollectionRef() {
    return collection(this.firestore, "threads");
  }

  async getAllThreads() {
    const threadsQuery = query(this.getThreadsCollectionRef());
    return getDocs(threadsQuery);
  }

  async createThread(title, content) {
    const threadsCollectionRef = this.getThreadsCollectionRef();

    const newThread = {
      title,
      content,
      createdAt: new Date(),
    };

    return addDoc(threadsCollectionRef, newThread);
  }

  async getThreadPosts(threadId) {
    const threadRef = collection(this.firestore, "threads", threadId);
    const postsQuery = query(collection(threadRef, "posts"));
    return getDocs(postsQuery);
  }

  async addPost(threadId, content) {
    const threadRef = collection(this.firestore, "threads", threadId);
    const postsCollectionRef = collection(threadRef, "posts");

    const newPost = {
      content,
      createdAt: new Date(),
    };

    return addDoc(postsCollectionRef, newPost);
  }

  async editThread(threadId, newData) {
    const threadRef = collection(this.firestore, "threads").doc(threadId);
    return updateDoc(threadRef, newData);
  }

  async deleteThread(threadId) {
    const threadRef = collection(this.firestore, "threads", threadId);
    return deleteDoc(threadRef);
  }
}

export default new ForumService();

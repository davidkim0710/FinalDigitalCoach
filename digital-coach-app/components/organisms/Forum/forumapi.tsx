import {
  addDoc,
  collection,
  DocumentReference,
  Firestore,
  getDocs,
  getFirestore,
  query,
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
}

export default new ForumService();

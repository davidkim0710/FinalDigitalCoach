import {
  addDoc,
  collection,
  deleteDoc,
  DocumentReference,
  Firestore,
  doc,
  getDoc,
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

  async createThread(title, content, name, id) {
    const threadsCollectionRef = this.getThreadsCollectionRef();

    const newThread = {
      title,
      content,
      createdAt: new Date(),
      author: name,
      authorID: id
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

  async editThread(threadId, title, content) {
    const threadRef = doc(collection(this.firestore, "threads"), threadId);
    const newData = {
      title,
      content,
      createdAt: new Date(),
    };
    return updateDoc(threadRef, newData);
}


  async deleteThread(threadId) {
    const threadRef = doc(this.firestore, "threads", threadId); // Construct a reference to the specific thread document
  
    if (!threadRef) throw new Error("Error deleting thread: Thread not found!");
  
    return deleteDoc(threadRef);
  }

}

export default new ForumService();

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
  
  private getCommentsCollectionRef(threadId: string) {
    console.log(threadId);
    return collection(this.firestore, "threads", threadId, "comments");
  }

  async getAllThreads() {
    const threadsQuery = query(this.getThreadsCollectionRef());
    return getDocs(threadsQuery);
  }
  async getAllThreadsWithComments() {
    const threadsQuery = query(this.getThreadsCollectionRef());
    const threadsSnapshot = await getDocs(threadsQuery);
    const threadsWithComments = [];
    for (const docRef of threadsSnapshot.docs) {
        const thread = docRef.data();
        const commentsQuery = query(this.getCommentsCollectionRef(docRef.id));
        const commentsSnapshot = await getDocs(commentsQuery);
        const comments = commentsSnapshot.docs.map(commentDoc => ({
            id: commentDoc.id,
            ...commentDoc.data()
        }));
        thread.comments = comments;
        threadsWithComments.push(thread);
    }
    console.log(threadsWithComments)
    return threadsWithComments;
}


  async createThread(title, content, name, id, alumni) {
    const threadsCollectionRef = this.getThreadsCollectionRef();

    const newThread = {
      title,
      content,
      createdAt: new Date(),
      author: name,
      authorID: id,
      alumni: alumni
    };

    return addDoc(threadsCollectionRef, newThread);
  }

  async addComment(threadId, content, name, id) {
    console.log(threadId);
    const commentsCollectionRef = this.getCommentsCollectionRef(threadId);

    const newComment = {
      content,
      createdAt: new Date(),
      author: name,
      authorID: id
    };

    return addDoc(commentsCollectionRef, newComment);
  }

  async getThreadPosts(threadId) {
    const threadRef = collection(this.firestore, "threads", threadId);
    const postsQuery = query(collection(threadRef, "posts"));
    return getDocs(postsQuery);
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

  async deleteComment(threadId, commentId) {
    const commentRef = doc(this.firestore, "threads", threadId, "comments", commentId);
    if (!commentRef) throw new Error("Error deleting comment: Comment not found!");
    return deleteDoc(commentRef);
  }

}

export default new ForumService();

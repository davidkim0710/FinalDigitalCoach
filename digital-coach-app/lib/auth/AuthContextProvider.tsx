import { PropsWithChildren, useEffect, useMemo, useState } from "react";
import AuthService from "./AuthService";
import { AuthContext } from "./AuthContext";
import UserService from "../user/UserService";
import { IUser } from "../user/models";
import { DocumentSnapshot } from "firebase/firestore";

export function AuthContextProvider({ children }: PropsWithChildren<{}>) {
  const [currentUser, setCurrentUser] =
    useState<DocumentSnapshot<IUser> | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    AuthService.onAuthStateChanged(async (user) => {
      if (user) {
        const userDocSnapshot = await UserService.getUser(user?.uid);

        setCurrentUser(userDocSnapshot);
      }
    });
  }, []);

  const providerValue = useMemo(() => {
    const login = async (email: string, password: string) => {
      try {
        const { user } = await AuthService.login(email, password);
        const userDocSnapshot = await UserService.getUser(user.uid);

        setCurrentUser(userDocSnapshot);
      } catch (error: any) {
        setError(error.message);
      }
    };

    // const loginWithGoogle = async () => {
    //   try {
    //     const { user } = await AuthService.loginWithGoogle();
    //     const userDocSnapshot = await UserService.getUser(user.uid);

    //     setCurrentUser(userDocSnapshot);
    //   } catch (error: any) {
    //     setError(error.message);
    //   }
    // };

    const signup = async (email: string, password: string) => {
      try {
        const { user } = await AuthService.signup(email, password);

        await UserService.createNewUser(user);

        const userDocSnapshot = await UserService.getUser(user.uid);

        setCurrentUser(userDocSnapshot);
      } catch (error: any) {
        setError(error.message);
      }
    };

    const logout = async () => {
      setCurrentUser(null);

      await AuthService.logout();
    };

    const fetchUser = async (userId: string = currentUser!.id) => {
      const userDocSnapshot = await UserService.getUser(userId);
      setCurrentUser(userDocSnapshot);
    };

    return {
      currentUser,
      setCurrentUser,
      error,
      login,
      signup,
      // loginWithGoogle,
      logout,
      fetchUser,
    };
  }, [currentUser, setCurrentUser, error]);

  return (
    <AuthContext.Provider value={providerValue}>
      {children}
    </AuthContext.Provider>
  );
}

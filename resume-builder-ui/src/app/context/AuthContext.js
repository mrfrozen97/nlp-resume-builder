"use client";

import { createContext, useContext, useEffect, useState } from 'react';
import { 
  onAuthStateChanged, 
  signInWithPopup, 
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  GoogleAuthProvider, 
  signOut 
} from 'firebase/auth';
import { auth } from '../firebase';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
    });
    return () => unsubscribe();
  }, []);

  // Google Sign-In
  const signInWithGoogle = () => {
    const provider = new GoogleAuthProvider();
    return signInWithPopup(auth, provider);
  };

  // Sign-In with Email and Password
  const signInWithEmail = (email, password) => {
    return signInWithEmailAndPassword(auth, email, password);
  };

  // Sign-Up and Login with Email and Password
  const signUpWithEmail = async (email, password) => {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      return userCredential;
    } catch (error) {
      if (error.code === 'auth/email-already-in-use') {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        return userCredential; 
      } else {
        throw error; 
      }
    }
  };

  // Log-Out
  const logOut = () => {
    return signOut(auth);
  };

  return (
    <AuthContext.Provider value={{ user, signInWithGoogle, signInWithEmail, signUpWithEmail, logOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

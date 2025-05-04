"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation"; 
import { useAuth } from "../context/AuthContext";

const SignUpPage = () => {
  const { signInWithGoogle, signUpWithEmail } = useAuth();
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const router = useRouter(); 
  const handleEmailSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await signUpWithEmail(email, password); 
      router.push("/resume-parser"); 
    } catch (error: any) {
      alert(error.message); 
    }
  };

  const handleGoogleSignIn = async () => {
    try {
      await signInWithGoogle();
      router.push("/upload"); 
    } catch (error: any) {
      alert(error.message);
    }
  };

  return (
    <div className="w-full h-[calc(100vh-var(--top-nav-bar-height))] flex items-center justify-center p-4">
      <div className="relative bg-zinc-300 rounded-[50px] w-full max-w-xl p-10 flex flex-col items-center">
        <h1 className="text-4xl font-normal text-black mb-10">Sign Up</h1>

        {/* Form */}
        <form className="w-full flex flex-col gap-6" onSubmit={handleEmailSignUp}>
          <div className="flex flex-col gap-2">
            <label htmlFor="email" className="text-xl font-normal text-black">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-white rounded-[20px] p-3 text-black text-lg focus:outline-none focus:ring-2 focus:ring-purple-700"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label htmlFor="password" className="text-xl font-normal text-black">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-white rounded-[20px] p-3 text-black text-lg focus:outline-none focus:ring-2 focus:ring-purple-700"
            />
          </div>

          <button
            type="submit"
            className="w-1/2 self-center bg-purple-700 rounded-[20px] border border-black text-purple-950 font-bold text-xl py-3 hover:bg-purple-800 transition-colors"
          >
            Sign Up
          </button>
        </form>

        {/* Divider */}
        <div className="flex items-center my-8 w-full">
          <div className="flex-grow h-px bg-black" />
          <span className="px-4 text-black text-xl font-normal">OR</span>
          <div className="flex-grow h-px bg-black" />
        </div>

        {/* Sign up with Google */}
        <button
          type="button"
          className="bg-purple-700 text-black text-xl font-normal rounded-2xl py-3 px-6 w-3/4 hover:bg-purple-800 transition-colors"
          onClick={handleGoogleSignIn} 
        >
          Sign Up with Google
        </button>
        <div className="mt-8 text-black text-lg">
        Already have an account?{" "}
        <a
            href="/login"
            className="text-purple-800 underline hover:text-purple-950 transition-colors"
        >
            Log in
        </a>
        </div>
      </div>
    </div>
  );
};

export default SignUpPage;

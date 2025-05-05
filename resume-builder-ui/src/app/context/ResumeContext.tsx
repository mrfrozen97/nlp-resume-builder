"use client";
import React, { createContext, useContext, useState, ReactNode } from "react";

interface ResumeContextType {
  resume: any; // you can replace `any` with your Resume type if you have it
  setResume: (resume: any) => void;
}

interface JobDescriptionContextType {
  resumeJD: any; // you can replace `any` with your Resume type if you have it
  setResumeJD: (resumeJD: any) => void;
}

const ResumeContext = createContext<ResumeContextType | undefined>(undefined);
const JobDescriptionContext = createContext<JobDescriptionContextType | undefined>(undefined);
const OptimizedResumeContext = createContext<JobDescriptionContextType | undefined>(undefined);

export function ResumeProvider({ children }: { children: ReactNode }) {
  const [resume, setResume] = useState<any>(null);

  return (
    <ResumeContext.Provider value={{ resume, setResume }}>
      {children}
    </ResumeContext.Provider>
  );
}

export function JobDescriptionProvider({ children }: { children: ReactNode }) {
  const [resumeJD, setResumeJD] = useState<any>(null);

  return (
    <JobDescriptionContext.Provider value={{ resumeJD, setResumeJD }}>
      {children}
    </JobDescriptionContext.Provider>
  );
}

export function OptimizedResumeProvider({ children }: { children: ReactNode }) {
  const [resumeJD, setResumeJD] = useState<any>(null);

  return (
    <OptimizedResumeContext.Provider value={{ resumeJD, setResumeJD }}>
      {children}
    </OptimizedResumeContext.Provider>
  );
}

export function useJobDescription() {
  const context = useContext(JobDescriptionContext);
  if (!context) {
    throw new Error("useResume must be used inside a ResumeProvider");
  }
  return context;
}

export function useOptimizedResume() {
  const context = useContext(OptimizedResumeContext);
  if (!context) {
    throw new Error("useResume must be used inside a ResumeProvider");
  }
  return context;
}

export function useResume() {
  const context = useContext(ResumeContext);
  if (!context) {
    throw new Error("useResume must be used inside a ResumeProvider");
  }
  return context;
}

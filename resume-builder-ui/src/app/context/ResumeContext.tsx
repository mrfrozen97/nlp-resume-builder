"use client";
import React, { createContext, useContext, useState, ReactNode } from "react";

interface ResumeContextType {
  resume: any; // you can replace `any` with your Resume type if you have it
  setResume: (resume: any) => void;
}

const ResumeContext = createContext<ResumeContextType | undefined>(undefined);

export function ResumeProvider({ children }: { children: ReactNode }) {
  const [resume, setResume] = useState<any>(null);

  return (
    <ResumeContext.Provider value={{ resume, setResume }}>
      {children}
    </ResumeContext.Provider>
  );
}

export function useResume() {
  const context = useContext(ResumeContext);
  if (!context) {
    throw new Error("useResume must be used inside a ResumeProvider");
  }
  return context;
}

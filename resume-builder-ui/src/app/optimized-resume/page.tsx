"use client";

import { MarkdownViewer } from "components/MarkdownViewer";
import { useOptimizedResume } from "context/ResumeContext";


export default function MarkdownDemoPage() {
    const {resumeJD} = useOptimizedResume();

  return (
    <main className="min-h-scree py-10 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
            📘 Optimized Resume
          </h1>
          <MarkdownViewer content={resumeJD} />
        </div>
      </div>
    </main>
  );
}

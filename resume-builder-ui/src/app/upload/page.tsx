"use client";

import { useState } from "react";
import { ResumeDropzone } from "../components/ResumeDropzone"; 
const UploadPage = () => {
  const [uploadedFileUrl, setUploadedFileUrl] = useState("");

  return (
    <div className="flex min-h-[calc(100vh-var(--top-nav-bar-height))] items-start justify-center pt-20 md:pt-48 p-4">
      <div className="w-full max-w-2xl rounded-lg p-10">
        <h1 className="text-3xl md:text-4xl font-bold text-center text-gray-100 mb-8">
          Upload Your Resume
        </h1>

        {/* Dropzone */}
        <ResumeDropzone onFileUrlChange={(url) => setUploadedFileUrl(url)} />

        {/* Uploaded file preview */}
        {uploadedFileUrl && (
          <div className="mt-8 text-center">
            <p className="text-green-400 font-semibold">Resume file is ready!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;

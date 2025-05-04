"use client";

import { useState } from "react";
import { LockClosedIcon } from "@heroicons/react/24/solid";
import { XMarkIcon } from "@heroicons/react/24/outline";
import { useRouter } from "next/navigation";
import Image from "next/image";

import addPdfSrc from "public/assets/add-pdf.svg";
import { parseResumeFromPdf } from "lib/parse-resume-from-pdf";
import { getHasUsedAppBefore, saveStateToLocalStorage } from "lib/redux/local-storage";
import { initialSettings, type ShowForm } from "lib/redux/settingsSlice";
import { cx } from "lib/cx";
import { deepClone } from "lib/deep-clone";

const defaultFileState = {
  name: "",
  size: 0,
  fileUrl: "",
};

const getFileSizeString = (size: number) => {
  const kb = size / 1024;
  const mb = kb / 1024;
  return kb < 1000 ? `${kb.toPrecision(3)} KB` : `${mb.toPrecision(3)} MB`;
};

interface ResumeDropzoneProps {
  onFileUrlChange: (fileUrl: string) => void;
  onFileChange?: (file: File) => void;
  className?: string;
  playgroundView?: boolean;
}

export const ResumeDropzone = ({
  onFileUrlChange,
  onFileChange,
  className,
  playgroundView = false,
}: ResumeDropzoneProps) => {
  const [file, setFile] = useState(defaultFileState);
  const [isHovered, setIsHovered] = useState(false);
  const [hasNonPdfFile, setHasNonPdfFile] = useState(false);
  const router = useRouter();

  const hasFile = Boolean(file.name);

  const handleFileSelect = (newFile: File) => {
    if (file.fileUrl) URL.revokeObjectURL(file.fileUrl);

    const fileUrl = URL.createObjectURL(newFile);
    setFile({ name: newFile.name, size: newFile.size, fileUrl });

    onFileUrlChange(fileUrl);
    onFileChange?.(newFile);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const newFile = event.dataTransfer.files[0];
    if (newFile?.name.toLowerCase().endsWith(".pdf")) {
      setHasNonPdfFile(false);
      handleFileSelect(newFile);
    } else {
      setHasNonPdfFile(true);
    }
    setIsHovered(false);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newFile = event.target.files?.[0];
    if (newFile) {
      if (newFile.name.toLowerCase().endsWith(".pdf")) {
        setHasNonPdfFile(false);
        handleFileSelect(newFile);
      } else {
        setHasNonPdfFile(true);
      }
    }
  };

  const removeFile = () => {
    setFile(defaultFileState);
    onFileUrlChange("");
  };

  const handleImport = async () => {
    const resume = await parseResumeFromPdf(file.fileUrl);
    const settings = deepClone(initialSettings);

    if (getHasUsedAppBefore()) {
      const sectionMap: Record<ShowForm, boolean> = {
        workExperiences: resume.workExperiences.length > 0,
        educations: resume.educations.length > 0,
        projects: resume.projects.length > 0,
        skills: resume.skills.descriptions.length > 0,
        custom: resume.custom.descriptions.length > 0,
      };

      for (const section in settings.formToShow) {
        settings.formToShow[section as ShowForm] = sectionMap[section as ShowForm];
      }
    }

    saveStateToLocalStorage({ resume, settings });
    router.push("/resume-builder");
  };

  return (
    <div
      className={cx(
        "flex justify-center rounded-md border-2 border-dashed border-gray-300 px-6",
        isHovered && "border-sky-400",
        playgroundView ? "pb-6 pt-4" : "py-12",
        className
      )}
      onDragOver={(e) => {
        e.preventDefault();
        setIsHovered(true);
      }}
      onDragLeave={() => setIsHovered(false)}
      onDrop={handleDrop}
    >
      <div className={cx("text-center", playgroundView ? "space-y-2" : "space-y-3")}>
        {!playgroundView && (
          <Image src={addPdfSrc} className="mx-auto h-14 w-14" alt="Add PDF" priority />
        )}

        {!hasFile ? (
          <>
            <p className={cx("pt-3 text-gray-400", !playgroundView && "text-lg font-semibold")}>
              Browse a PDF file or drop it here
            </p>
            <p className="flex justify-center text-sm text-gray-500">
              <LockClosedIcon className="mr-1 mt-1 h-3 w-3 text-gray-400" />
              File data is used locally and never leaves your browser
            </p>
          </>
        ) : (
          <div className="flex items-center justify-center gap-3 pt-3">
            <div className="pl-7 font-semibold text-gray-900">
              {file.name} - {getFileSizeString(file.size)}
            </div>
            <button
              type="button"
              className="outline-theme-blue rounded-md p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-500"
              title="Remove file"
              onClick={removeFile}
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>
        )}

        <div className="pt-4">
          {!hasFile ? (
            <>
              <label
                className={cx(
                  "bg-accentPurple text-white cursor-pointer rounded-full px-6 pb-2.5 pt-2 font-semibold shadow-sm",
                  playgroundView ? "border" : "bg-accentPurple"
                )}
              >
                Browse file
                <input
                  type="file"
                  className="sr-only"
                  accept=".pdf"
                  onChange={handleInputChange}
                />
              </label>
              {hasNonPdfFile && (
                <p className="mt-6 text-red-400">Only PDF files are supported</p>
              )}
            </>
          ) : (
            <>
              {!playgroundView && (
                <button
                  type="button"
                  className="bg-accentPurple text-white cursor-pointer rounded-full px-6 pb-2.5 pt-2 font-semibold shadow-sm"
                  onClick={handleImport}
                >
                  Import and Continue <span aria-hidden="true">→</span>
                </button>
              )}
              <p className={cx("text-gray-500", !playgroundView && "mt-6")}>
                Note: {playgroundView ? "Parser" : "Import"} works best on single column resumes
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

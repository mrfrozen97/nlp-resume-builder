"use client";
import { useState, useEffect, useMemo } from "react";
import { readPdf } from "lib/parse-resume-from-pdf/read-pdf";
import type { TextItems } from "lib/parse-resume-from-pdf/types";
import { groupTextItemsIntoLines } from "lib/parse-resume-from-pdf/group-text-items-into-lines";
import { groupLinesIntoSections } from "lib/parse-resume-from-pdf/group-lines-into-sections";
import { extractResumeFromSections } from "lib/parse-resume-from-pdf/extract-resume-from-sections";
import { ResumeDropzone } from "components/ResumeDropzone";
import { cx } from "lib/cx";
import { Heading, Link, Paragraph } from "components/documentation";
import { ResumeTable } from "resume-parser/ResumeTable";
import { FlexboxSpacer } from "components/FlexboxSpacer";
import { useResume, useJobDescription } from "context/ResumeContext";

const RESUME_EXAMPLES = [
  {
    fileUrl: "resume-example/laverne-resume.pdf",
    description: (
      <span>
        Borrowed from University of La Verne Career Center -{" "}
        <Link href="https://laverne.edu/careers/wp-content/uploads/sites/15/2010/12/Undergraduate-Student-Resume-Examples.pdf">
          Link
        </Link>
      </span>
    ),
  },
  {
    fileUrl: "resume-example/openresume-resume.pdf",
    description: (
      <span>
        Created with OpenResume resume builder -{" "}
        <Link href="/resume-builder">Link</Link>
      </span>
    ),
  },
];

const defaultFileUrl = RESUME_EXAMPLES[0]["fileUrl"];

export default function ResumeParser() {
  const [fileUrl, setFileUrl] = useState(defaultFileUrl);
  const [textItems, setTextItems] = useState<TextItems>([]);
  const lines = useMemo(() => groupTextItemsIntoLines(textItems), [textItems]);
  const sections = useMemo(() => groupLinesIntoSections(lines), [lines]);
  const { resume, setResume } = useResume();
  const { resumeJD, setResumeJD } = useJobDescription();
  const parsedResume = useMemo(() => extractResumeFromSections(sections), [sections]);
  const [input, setInput] = useState(resumeJD);

  useEffect(() => {
    if (input && input.length > 50) {
      setResumeJD(input);
    }
  }, [input, setResumeJD]);

  useEffect(() => {
    if (parsedResume) {
      console.log(parsedResume);
      setResume(parsedResume);
    }
  }, [parsedResume]);

  useEffect(() => {
    async function test() {
      const textItems = await readPdf(fileUrl);
      setTextItems(textItems);
    }
    test();
  }, [fileUrl]);

  const uploadFileToServer = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload_file", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();
      console.log("File uploaded to server:", data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <main className="h-full w-full overflow-hidden">
      <div className="grid md:grid-cols-6">
        <div className="flex justify-center px-2 md:col-span-3 md:h-[calc(100vh-var(--top-nav-bar-height))] md:justify-end">
          <section className="mt-5 grow px-4 md:max-w-[600px] md:px-0">
            <div className="aspect-h-[9.5] aspect-w-7">
              <iframe src={`${fileUrl}#navpanes=0`} className="h-full w-full" />
            </div>
          </section>
          <FlexboxSpacer maxWidth={45} className="hidden md:block" />
        </div>
        <div className="flex px-6 text-gray-900 md:col-span-3 md:h-[calc(100vh-var(--top-nav-bar-height))] md:overflow-y-scroll">
          <FlexboxSpacer maxWidth={45} className="hidden md:block" />
          <section className="max-w-[600px] grow">
            <div className="mt-3">
              <ResumeDropzone
                onFileUrlChange={(fileUrl) =>
                  setFileUrl(fileUrl || defaultFileUrl)
                }
                onFileChange={(file) => {
                  if (file) {
                    uploadFileToServer(file);
                  }
                }}
                playgroundView={true}
              />
            </div>
            <div className="flex flex-col gap-2" style={{ paddingTop: "20px" }}>
              <Heading level={2} className="!mt-[1.2em]">
                Enter Job Description
              </Heading>
              <textarea
                id="jd-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Paste or type the job description here..."
                className="border border-gray-300 p-2 rounded-md min-h-[100px]"
              />
            </div>
            <Heading level={2} className="!mt-[1.2em]">
              Resume Parsing Results
            </Heading>
            <ResumeTable resume={resume} />
            <div className="pt-24" />
          </section>
        </div>
      </div>
    </main>
  );
}

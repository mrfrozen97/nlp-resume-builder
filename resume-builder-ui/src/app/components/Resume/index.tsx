"use client";
import { useState, useMemo } from "react";
import { ResumeIframeCSR } from "components/Resume/ResumeIFrame";
import { ResumePDF } from "components/Resume/ResumePDF";
import {
  ResumeControlBarCSR,
  ResumeControlBarBorder,
} from "components/Resume/ResumeControlBar";
import { FlexboxSpacer } from "components/FlexboxSpacer";
import { useAppSelector } from "lib/redux/hooks";
import { selectSettings } from "lib/redux/settingsSlice";
import { DEBUG_RESUME_PDF_FLAG } from "lib/constants";
import {
  useRegisterReactPDFFont,
  useRegisterReactPDFHyphenationCallback,
} from "components/fonts/hooks";
import { NonEnglishFontsCSSLazyLoader } from "components/fonts/NonEnglishFontsCSSLoader";
import { useResume } from "context/ResumeContext"; // <-- custom resume context

export const Resume = () => {
  const [scale, setScale] = useState(0.8);
  const { resume } = useResume(); // <-- using context for resume
  const settings = useAppSelector(selectSettings); // <-- still using Redux for settings

  const document = useMemo(
    () => <ResumePDF resume={resume} settings={settings} isPDF={true} />,
    [resume, settings]
  );

  useRegisterReactPDFFont();
  useRegisterReactPDFHyphenationCallback(settings.fontFamily);

  return (
    <>
      <NonEnglishFontsCSSLazyLoader />
      <div
        className="relative flex justify-center md:justify-start"
        style={{ width: "1200px" }} // Increased width here
      >
        <FlexboxSpacer maxWidth={500} className="hidden md:block" />
        <div className="relative inline-block"
    style={{ width: "1200px", textAlign: "center", paddingLeft: "10%" }}>
          <section className="">
            <ResumeIframeCSR
              documentSize={settings.documentSize}
              scale={scale}
              enablePDFViewer={DEBUG_RESUME_PDF_FLAG}
            >
              <ResumePDF
                resume={resume}
                settings={settings}
                isPDF={DEBUG_RESUME_PDF_FLAG}
              />
            </ResumeIframeCSR>
          </section>
          <ResumeControlBarCSR
            scale={scale}
            setScale={setScale}
            documentSize={settings.documentSize}
            document={document}
            fileName={(resume && resume.profile.name) + " - Resume"}
          />
        </div>
        <ResumeControlBarBorder />
      </div>
    </>
  );
};

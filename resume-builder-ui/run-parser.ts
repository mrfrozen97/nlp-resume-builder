// run-parser.ts
import fs from "fs";
import path from "path";

// // Adjust the import path to point correctly based on your project structure
// import { extractSectionsFromText } from "./src/app/lib/parse-resume-from-pdf/extract-resume-from-sections";
  


import type {
    TextItem,
    Line,
    Lines,
    ResumeSectionToLines,
  } from "./src/app/lib/parse-resume-from-pdf/types";
  import { extractResumeFromSections } from "./src/app/lib/parse-resume-from-pdf/extract-resume-from-sections";
  
  // Simulate Step 1: convert raw text to text items
  const readText = (text: string): TextItem[] => {
    const lines = text.split(/\r?\n/).filter(Boolean);
    let y = 0;
    return lines.flatMap(line => {
      const item: TextItem = {
        text: line.trim(),
        x: 0,
        y: y += 10,
        width: line.length * 6,
        height: 10,
        fontName: "mockFont",
        hasEOL: true,
      };
      return [item];
    });
  };
  
  // Simulate Step 2: group text items into lines
  const groupTextItemsIntoLines = (textItems: TextItem[]): Lines => {
    return textItems.map(item => [item]); // each TextItem is its own line
  };
  
  // Simulate Step 3: group lines into sections based on keywords
  const groupLinesIntoSections = (lines: Lines): ResumeSectionToLines => {
    const sectionHeaders = ["education", "experience", "skills", "projects", "profile"];
    const sections: ResumeSectionToLines = {};
    let currentSection = "other";
  
    for (const line of lines) {
      const lineText = line[0]?.text?.toLowerCase() ?? "";
      if (sectionHeaders.includes(lineText)) {
        currentSection = lineText;
        if (!sections[currentSection]) sections[currentSection] = [];
      } else {
        if (!sections[currentSection]) sections[currentSection] = [];
        sections[currentSection].push(line);
      }
    }
  
    return sections;
  };
  
  // Main method: raw text parser that mimics PDF parser flow
  export const parseResumeFromText = (resumeText: string) => {
    const textItems = readText(resumeText);
    const lines = groupTextItemsIntoLines(textItems);
    const sections = groupLinesIntoSections(lines);
    const resume = extractResumeFromSections(sections);
    return resume;
  };
  

// Read your raw resume text from a file
const resumeText = fs.readFileSync("resume.txt", "utf8");

// Call the extractor function
const sections = parseResumeFromText(resumeText);

console.log(JSON.stringify(sections, null, 2));

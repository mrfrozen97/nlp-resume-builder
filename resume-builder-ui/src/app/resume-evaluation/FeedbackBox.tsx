"use client";
import React, { useState } from "react";

const tagColors = [
  "bg-red-400/20 text-red-300 border-red-300",
  "bg-green-400/20 text-green-300 border-green-300",
  "bg-blue-400/20 text-blue-300 border-blue-300",
  "bg-yellow-400/20 text-yellow-300 border-yellow-300",
  "bg-purple-400/20 text-purple-300 border-purple-300",
  "bg-pink-400/20 text-pink-300 border-pink-300",
  "bg-orange-400/20 text-orange-300 border-orange-300",
];

const getColorClass = (index: number) => {
  return tagColors[index % tagColors.length];
};

type FeedbackBoxProps = {
  feedback: string;
  skills: string[];
  heading: string;
};

const FeedbackBox: React.FC<FeedbackBoxProps> = ({ feedback, skills, heading }) => {
  const [expanded, setExpanded] = useState(false);
  const MAX_LENGTH = 300;

  const isLong = feedback.length > MAX_LENGTH;
  const displayText = expanded || !isLong ? feedback : feedback.slice(0, MAX_LENGTH) + "...";

  return (
    <div className="w-full max-w-4xl p-6 rounded-2xl bg-white/10 text-white shadow-xl space-y-6">
      {/* Feedback section */}
      <div>
        <h2 className="text-2xl font-semibold mb-2">{heading}</h2>
        <div
            className={`whitespace-pre-line transition-all duration-300 ${
                expanded ? "max-h-[1000px]" : "max-h-[190px]"
            } overflow-hidden text-base space-y-2`}
            >
            {displayText.split("\n").map((line, idx) => (
                <p key={idx} className="leading-relaxed">
                {line}
                </p>
            ))}
            </div>

        {isLong && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="mt-2 text-sm text-blue-400 hover:underline"
          >
            {expanded ? "Show less" : "Read more"}
          </button>
        )}
      </div>

      {/* Skills section */}
      <div>
        <h2 className="text-2xl font-semibold mb-2">Job Matching Skills</h2>
        <div className="flex flex-wrap gap-3">
          {skills.map((skill, index) => (
            <span
              key={index}
              className={`px-4 py-1 border rounded-full text-sm font-medium ${getColorClass(index)}`}
            >
              {skill}
            </span>
          ))}
          {
            skills.length==0 && <span
            key={0}
            className="px-4 py-1 border rounded-full text-sm font-medium bg-red-400/20 text-red-300 border-red-300">
            None Found
          </span>
          }
        </div>
      </div>
    </div>
  );
};

export default FeedbackBox;

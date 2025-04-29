"use client";

import React, { useState } from "react";

const getColor = (score: number) => {
  if (score >= 80) return "text-green-500 stroke-green-400";
  if (score >= 60) return "text-yellow-400 stroke-yellow-400";
  if (score >= 40) return "text-orange-400 stroke-orange-400";
  return "text-red-500 stroke-red-400";
};

const CircleProgress = ({ score }: { score: number }) => {
  const radius = 55;
  const stroke = 10;
  const normalizedRadius = radius - stroke / 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  const color = getColor(score);

  return (
    <svg height={radius * 2} width={radius * 2} className="rotate-[-90deg]">
      <circle
        stroke="#e5e7eb"
        fill="transparent"
        strokeWidth={stroke}
        r={normalizedRadius}
        cx={radius}
        cy={radius}
      />
      <circle
        className={`${color} transition-all duration-500`}
        fill="transparent"
        strokeWidth={stroke}
        strokeDasharray={circumference + " " + circumference}
        style={{ strokeDashoffset }}
        r={normalizedRadius}
        cx={radius}
        cy={radius}
      />
    </svg>
  );
};

export default function EvaluationPage() {
  const [overallScore, setOverallScore] = useState(74);
  const [skillScore, setSkillScore] = useState(65);
  const [impactScore, setImpactScore] = useState(83);
  const cardWIdth = 80;
  const cardHeight = 60;

  const [topMatchingSkills, setTopMatchingSkills] = useState([
    { skill: "Java", weight: 0.56 },
    { skill: "Python", weight: 0.63 },
    { skill: "Leadership", weight: 0.29 },
  ]);

  const [topMissingSkills, setTopMissingSkills] = useState([
    { skill: "SQL", weight: 0.76 },
    { skill: "Kubernetes", weight: 0.52 },
    { skill: "Git", weight: 0.15 },
    { skill: "MacOS", weight: 0.11 },
  ]);

  return (
    <div className="min-h-screen bg-[#37375b] p-10 text-white flex flex-col items-center space-y-10">
      <h1 className="text-4xl font-bold">Detailed Analysis</h1>

      {/* Scores Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Overall Score */}
        <div className="bg-white/10 p-6 rounded-2xl flex flex-col items-center space-y-4">
          <div className="relative w-60 h-50 flex items-center justify-center">
            <CircleProgress score={overallScore} />
            <span className="absolute text-xl font-semibold">{overallScore}/100</span>
          </div>
          <p className="text-xl">Overall Score</p>
        </div>

        {/* Skill Score */}
        <div className="bg-white/10 p-6 rounded-2xl flex flex-col items-center space-y-4">
          <div className="relative w-60 h-50 flex items-center justify-center">
            <CircleProgress score={skillScore} />
            <span className="absolute text-xl font-semibold">{skillScore}/100</span>
          </div>
          <p className="text-xl">Skill Score</p>
        </div>

        {/* Impact Score */}
        <div className="bg-white/10 p-6 rounded-2xl flex flex-col items-center space-y-4">
          <div className="relative w-60 h-50 flex items-center justify-center">
            <CircleProgress score={impactScore} />
            <span className="absolute text-xl font-semibold">{impactScore}/100</span>
          </div>
          <p className="text-xl">Impact Score</p>
        </div>
      </div>

      {/* Skills Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-5xl">
        {/* Top Matching Skills */}
        <div className="bg-white/10 p-6 rounded-2xl">
          <h2 className="text-2xl font-semibold mb-4">Top Matching Skills</h2>
          <div className="space-y-3">
            {topMatchingSkills.map((skill, idx) => (
              <div key={idx} className="flex justify-between items-center bg-green-200/20 p-3 rounded-xl">
                <span className="font-medium">{skill.skill}</span>
                <span className="font-mono">{skill.weight}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Top Missing Skills */}
        <div className="bg-white/10 p-6 rounded-2xl">
          <h2 className="text-2xl font-semibold mb-4">Top Missing Skills</h2>
          <div className="space-y-3">
            {topMissingSkills.map((skill, idx) => (
              <div key={idx} className="flex justify-between items-center bg-yellow-200/20 p-3 rounded-xl">
                <span className="font-medium">{skill.skill}</span>
                <span className="font-mono">{skill.weight}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

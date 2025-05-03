"use client";
import { useResume, useJobDescription } from "context/ResumeContext";
import React, { useEffect, useState } from "react";
import {resumeToText, workExToText, projectToText} from "lib/redux/types";
import FeedbackBox from "./FeedbackBox";
import ChatBotWidget from "components/ChatbotWidget";

const getColor = (score: number) => {
  if (score >= 80) return "text-green-500 stroke-green-400";
  if (score >= 60) return "text-yellow-400 stroke-yellow-400";
  if (score >= 40) return "text-orange-400 stroke-orange-400";
  return "text-red-500 stroke-red-400";
};



const CircleProgress = ({ score }: { score: number }) => {
  const radius = 60;
  const stroke = 12;
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
  const { resume } = useResume();
  const { resumeJD } = useJobDescription();
  const [topMatchingSkills, setTopMatchingSkills] = useState({
        "Java": 0.56,
        "Python": 0.63,
        "Leadership": 0.29 ,
    });

  const [topMissingSkills, setTopMissingSkills] = useState({
    "Java": 0.56,
    "Python": 0.63,
    "Leadership": 0.29 ,
});
  const [result, setResult] = useState<any>(null);
  const [workexFeedback, setWorkexFeedback] = useState<any>(null);
  const [projectFeedback, setProjectFeedback] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchScore = async (resumeText: string, jobDescription: string) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/score_resume', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription,
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error scoring resume:', error);
      setResult({  });
    } finally {
      setLoading(false);
    }
  };

  const fetchWorkexFeedBack = async (workexText: string, jobDescription: string) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/workex_feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          workex_text: workexText,
          job_description: jobDescription,
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setWorkexFeedback(data);
    } catch (error) {
      console.error('Error scoring resume:', error);
      setWorkexFeedback({  });
    } finally {
      setLoading(false);
    }
  };

  const fetchProjectFeedback = async (projectText: string, jobDescription: string) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/projectex_feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          project_text: projectText,
          job_description: jobDescription,
        }),
      });
  
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
  
      const data = await response.json();
      setProjectFeedback(data);
    } catch (error) {
      console.error('Error fetching project feedback:', error);
      setProjectFeedback({});
    } finally {
      setLoading(false);
    }
  };
  


  useEffect(() => {
    if (resume && resumeJD && resumeJD.length > 0) {
      //console.log(resumeToText(resume));
      fetchScore(resumeToText(resume), resumeJD);
      fetchWorkexFeedBack(workExToText(resume), resumeJD);
      fetchProjectFeedback(projectToText(resume), resumeJD);
    }
  }, [resume]);

  
  useEffect(()=>{
    if(result){
      if ("normalized_score" in result){
        setSkillScore(Math.round(result["normalized_score"]*100));
      }
      if ("matched_skills" in result){
        const sortedMatchedSkills = Object.entries(result["matched_skills"])
              .sort(([, a], [, b]) => b - a)
              .slice(0, 5)
              .reduce((acc, [key, value]) => {
                acc[key] = value;
                return acc;
              }, {} as typeof result["matched_skills"]);
        setTopMatchingSkills(sortedMatchedSkills);
      }
      if ("missing_skills" in result){
        const sortedMissingSkills = Object.entries(result["missing_skills"])
            .sort(([, a], [, b]) => b - a)            // sort by descending value
            .slice(0, 5)                              // take top 5 entries
            .reduce((acc, [key, value]) => {
              acc[key] = value;
              return acc;
            }, {} as typeof result["missing_skills"]);


        setTopMissingSkills(sortedMissingSkills);
      }
    }
  }, [result]);


  return (
    <div className="min-h-screen bg-[#37375b] p-10 text-white flex flex-col items-center space-y-10">
      <h1 className="text-4xl font-bold">Resume Analysis</h1>

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
          <div key={-1} className="flex justify-between items-cente p-3 rounded-xl" style={{backgroundColor: "rgba(100, 140, 60, 1)",}}>
                <span className="font-medium bold">{"Skills"}</span>
                <span className="font-mono bold">{"Weight"}</span>
          </div>
            {Object.entries(topMatchingSkills).map(([skill, score], idx) => (
              <div key={idx} className="flex justify-between items-center bg-green-200/20 p-3 rounded-xl">
                <span className="font-medium">{skill}</span>
                <span className="font-mono">{Math.round(score*1000)/10}</span>
              </div>
            ))}
            {(topMatchingSkills && Object.keys(topMatchingSkills).length==0 && <div key={1} className="flex justify-between items-center bg-green-200/20 p-3 rounded-xl">
                <span className="font-medium">{"None Found"}</span>
              </div>)}
          </div>
        </div>

        {/* Top Missing Skills */}
        <div className="bg-white/10 p-6 rounded-2xl">
          <h2 className="text-2xl font-semibold mb-4">Top Missing Skills</h2>
          <div className="space-y-3">
          <div key={-1} className="flex justify-between items-cente p-3 rounded-xl" style={{backgroundColor: "rgba(140, 100, 60, 1)",}}>
                <span className="font-medium">{"Skills"}</span>
                <span className="font-mono">{"Weight"}</span>
          </div>
            {Object.entries(topMissingSkills).map(([skill, score], idx) => (
              <div key={idx} className="flex justify-between items-center bg-yellow-200/20 p-3 rounded-xl">
                <span className="font-medium">{skill}</span>
                <span className="font-mono">{Math.round(score*1000)/10}</span>
              </div>
            ))}
            {(topMissingSkills && Object.keys(topMissingSkills).length==0 && <div key={1} className="flex justify-between items-center bg-yellow-200/20 p-3 rounded-xl">
                <span className="font-medium">{"None Found"}</span>
              </div>)}
          </div>
        </div>

      </div>
        {/* Work Experience FeedBack */}
        {workexFeedback && <FeedbackBox feedback={workexFeedback["feedback_text"]} skills={Object.keys(workexFeedback["matched_skills"])} heading={"Work Experience Feedback"}/>}
        {/* Project FeedBack */}
        {projectFeedback && (
          <FeedbackBox
            feedback={projectFeedback["feedback_text"]}
            skills={Object.keys(projectFeedback["matched_skills"])}
            heading={"Project Feedback"}
          />
        )}

      <ChatBotWidget />
    </div>
  );
}

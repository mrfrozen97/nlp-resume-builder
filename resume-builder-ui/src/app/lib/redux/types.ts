export interface ResumeProfile {
  name: string;
  email: string;
  phone: string;
  url: string;
  summary: string;
  location: string;
}

export interface ResumeWorkExperience {
  company: string;
  jobTitle: string;
  date: string;
  descriptions: string[];
}

export interface ResumeEducation {
  school: string;
  degree: string;
  date: string;
  gpa: string;
  descriptions: string[];
}

export interface ResumeProject {
  project: string;
  date: string;
  descriptions: string[];
}

export interface FeaturedSkill {
  skill: string;
  rating: number;
}

export interface ResumeSkills {
  featuredSkills: FeaturedSkill[];
  descriptions: string[];
}

export interface ResumeCustom {
  descriptions: string[];
}

export interface Resume {
  profile: ResumeProfile;
  workExperiences: ResumeWorkExperience[];
  educations: ResumeEducation[];
  projects: ResumeProject[];
  skills: ResumeSkills;
  custom: ResumeCustom;
}

export type ResumeKey = keyof Resume;


export const resumeToText = (resume: Resume): string => {
  const { profile, workExperiences, educations, projects, skills, custom } = resume;

  const profileText = `
  Name: ${profile.name}
  Email: ${profile.email}
  Phone: ${profile.phone}
  URL: ${profile.url}
  Location: ${profile.location}
  Summary: ${profile.summary}
  `;

  const workText = workExperiences.map((work, i) => `
  Work Experience #${i + 1}
  Company: ${work.company}
  Job Title: ${work.jobTitle}
  Date: ${work.date}
  Descriptions:
  ${work.descriptions.join("\n  ")}
  `).join("\n");

  const educationText = educations.map((edu, i) => `
  Education #${i + 1}
  School: ${edu.school}
  Degree: ${edu.degree}
  Date: ${edu.date}
  GPA: ${edu.gpa}
  Descriptions:
  ${edu.descriptions.join("\n  ")}
  `).join("\n");

  const projectText = projects.map((proj, i) => `
  Project #${i + 1}
  Name: ${proj.project}
  Date: ${proj.date}
  Descriptions:
  ${proj.descriptions.join("\n  ")}
  `).join("\n");

  const skillText = `
  Skills:
  Featured Skills:
  ${skills.featuredSkills.map(s => `- ${s.skill} (Rating: ${s.rating})`).join("\n  ")}
  Other Descriptions:
  ${skills.descriptions.join("\n  ")}
  `;

  const customText = `
  Custom:
  ${custom.descriptions.join("\n  ")}
  `;

  return [
    profileText,
    workText,
    educationText,
    projectText,
    skillText,
    customText
  ].join("\n\n");
};


export const workExToText = (resume: Resume): string => {
  const { profile, workExperiences, educations, projects, skills, custom } = resume;


  const workText = workExperiences.map((work, i) => `
  Company: ${work.company}
  Job Title: ${work.jobTitle}
  Date: ${work.date}
  Descriptions:
  ${work.descriptions.join("\n  ")}
  `).join("\n");

  return workText;
};


export const projectToText = (resume: Resume): string => {
  const { profile, workExperiences, educations, projects, skills, custom } = resume;

  const projectText = projects.map((proj, i) => `
  Project #${i + 1}
  Name: ${proj.project}
  Date: ${proj.date}
  Descriptions:
  ${proj.descriptions.join("\n  ")}
  `).join("\n");

  return projectText;
};
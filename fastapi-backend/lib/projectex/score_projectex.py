import subprocess

class ProjectEX:
    def __init__(self):
        pass

    def run_ollama_cli(self, prompt):
        process = subprocess.Popen(
            ['ollama', 'run', 'deepseek-r1:1.5b'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        stdout, stderr = process.communicate(input=prompt)
        return stdout

    def classify_output(self, text: str):
        positive = text.count("positive") + text.count("Positive")
        negative = text.count("negative") + text.count("Negative")
        return True if positive > negative else False

    def match_project_with_jd(self, jd, project):
        output = self.run_ollama_cli(
            f"{jd}\n\nClassify as positive if this job description is well matched with the following "
            f"project experience. Otherwise, classify negative. Be lenient and consider transferable skills.\n\n{project}"
        )
        return self.classify_output(output)

    def format_output(self, output):
        # Safely extract part after </think> if it exists
        if "</think>" in output:
            output = output.split("</think>")[1]
        return output.replace("**", "").strip()

    def get_project_feedback(self, jd, project):
        output = self.run_ollama_cli(
            f"{jd}\n\nEvaluate how well the below project matches the job description. "
            f"Provide brief feedback (max 50 words) on how to improve it: "
            f"Consider missing skills, technical depth, impact, or relevance.\n\n{project}"
        )
        return self.format_output(output)


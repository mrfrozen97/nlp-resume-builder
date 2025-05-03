import subprocess


class WorkEX:
    def __init__(self):
        pass

    def run_ollama_cli(self, prompt):
        process = subprocess.Popen(
            ['ollama', 'run', 'deepseek-r1:1.5b'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # 👈 This is key
            encoding='utf-8'
        )

        stdout, stderr = process.communicate(input=prompt)
        return stdout

    def classify_output(self, text: str):
        positive = text.count("positive") + text.count("Positive")
        negative = text.count("negative") + text.count("Negative")
        return True if positive > negative else False

    def match_workex_with_jd(self, jd, workex):
        output = self.run_ollama_cli(f"{jd} Classify positive if this job description matches this following"
                                     f" Job experience else"
                                f" classify negative, be lenient in evaluation {workex}")
        return self.classify_output(output)

    def format_output(self, output):
        output = output.split("</think>")[1]
        output = output.replace("**", "")
        return output

    def get_workex_feedback(self, jd, workex):
        output = self.run_ollama_cli(f"{jd} Check if this Job description matched the below work experience."
                                     f"Provide short (50 words) feedback on how to improve the work experience points"
                                     f"(like What skills are missing, if any? What impact words are missing, if any?)"
                                     f" {workex}")
        return self.format_output(output)


if __name__ == "__main__":

    workex = """Integral Ad Science (Nasdaq: IAS) (1 year 7 months)
Software Intern July 2022 - May 2023
● Designed and Engineered an SDK for Unity 3D and Unreal gaming engines. Filed 4 patents for this work.
● Designed and Implemented a web crawling code/algorithm that could crawl and store data for 3.6 million apps on
Play Store and App Store within 24 hours and update the data every 12 hours, making it 50% faster.
● Conducted a global technical information session for all tech employees on Spark streaming data pipelines in
Databricks, covering the implementation of streaming aggregations, pipeline monitoring, and delta tables."""
    jd = """What You Will Do

Assist in designing and implementing tools to detect sensitive information in application logs
Develop and train machine learning models using internal sensitive logs to improve detection accuracy
Implement log masking techniques to protect sensitive data before forwarding to log backends
Contribute to the development of observability pipelines for collecting, processing, and analyzing telemetry data
Collaborate with team members to integrate sensitive data detection and masking into existing logging frameworks
Help create and maintain dashboards for monitoring the effectiveness of sensitive data detection and masking
Participate in code reviews and contribute to best practices for log management and data protection
Assist in troubleshooting and resolving issues related to log processing and sensitive data handling

Who You Are

Master’s degree in computer science, Software Engineering, or a related field
Solid knowledge of Python or Golang for building high-quality software.
Knowledge and/or Experience in software engineering, with a focus on observability and monitoring with basic understanding of observability concepts, including logs, metrics, and distributed tracing
Familiarity/Experience with AWS Cloud (EC2, ECS, EKS, S3, ALB, CloudWatch, Rekognition) and containerization technologies (Docker, Kubernetes)
Knowledge of distributed systems and microservices architectures
Strong analytical and problem-solving skills
Excellent communication and collaboration abilities
Nice to have basic exposure with Application Performance Monitoring (APM) tools such as Datadog, New Relic, or Dynatrace
Nice to have open-source contributions with Open Telemetry or similar open-source observability frameworks or tools
Nice to have Familiarity with CI/CD pipelines and DevOps practices
Nice to have knowledge of machine learning techniques for anomaly detection and root cause analysis
"""

    obj = WorkEX()
    print(obj.match_workex_with_jd(jd, workex))
    print(obj.get_workex_feedback(jd, workex))

## Overview

This README shows the minimal steps to install Ollama locally, pull the required model, start the Ollama server, and run the resume optimizer script.

## 1. Install Ollama

* **macOS / Linux**

  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

  ([Ollama][1])

* **Windows**
  Download and run the installer from the official site:
  [https://ollama.com/download](https://ollama.com/download)
  ([Medium][2])

## 2. Pull the LLM Model

Once Ollama is installed, pull the DeepSeek-R1 model you want to use (e.g. 1.5B parameters):

```bash
ollama pull deepseek-r1:1.5b
ollama pull deepseek-r1:7b
```

> ### note:  at the starting of resume_optimizer_v2.py file please edit the model name if you want to change it. defailt is the deepseek-r1:7b model.

## 3. Start the Ollama Server

Run the local server so your script can send requests:

```bash
ollama serve
```

([GitHub][3])

You should see a message like:

```
Listening on 127.0.0.1:11434
```

## 4. Run the Resume Optimizer

With the server running, invoke the Python CLI script:

```bash
python scripts/llm/resume_optimizer_v2.py \
  --resume my_resume.txt \
  --job_desc posting.txt \
  --extracted extracted_data.json \
  --output optimized.txt
```

* **--resume**: path to your original resume text
* **--job\_desc**: path to the job description text
* **--extracted**: path to the pre-extracted keywords JSON
* **--output**: path where the optimized resume will be written

You’ll see a line like:

```
Selected bucket: data_science
Optimized resume written to optimized.txt
```

---

That’s it—now you can optimize resumes entirely on-premise with Ollama!

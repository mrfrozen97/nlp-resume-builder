import re

CS_Comprehensive_List = [
    'Ethical AI', 'Authentication', 'Asana', 'Fuzzy Logic', 'A/B Testing', 'Webpack', 'BERT', 'Quantum Computing',
    'JUnit', 'Jupyter Notebooks', 'Disaster Recovery', 'Language Models', 'Web Scraping', 'Cybersecurity', 'MongoDB',
    'Data Mining', 'CI/CD Pipelines', 'Data Lakes', 'SQL', 'DevOps', 'Kanban', 'Data Privacy', 'System Design',
    'Full Stack Development', 'Data Pipelines', 'Data Visualization', 'Cloud Security', 'Cloud Computing', 'DevSecOps',
    'Mentorship', 'NumPy', 'JIRA', 'Express.js', 'Customer-Facing Skills', 'GPT', 'Amazon Web Services', 'Agile',
    'Text Preprocessing', 'Scrum', 'Model Deployment', 'PyTorch', 'Communication', 'Function-as-a-Service (FaaS)',
    'Cloud Deployment', 'Classification', 'Sequence Modeling', 'Vue.js', 'Concurrency', 'Matplotlib',
    'Behavior-Driven Development (BDD)', 'Version Control', 'Security', 'Flask', 'Google Cloud Platform',
    'Transformer Models', 'Business Intelligence (BI)', 'D3.js', 'MPI', 'CUDA', 'Go', 'PCI-DSS', 'FPGAs',
    'Lemmatization', 'Django', 'Blue Teaming', 'Apache', 'Graph Databases', 'SOLID Principles', 'NLP',
    'Agile Project Management', 'Frontend Development', 'SciPy', 'Jenkins', 'Collaboration', 'Firewalls',
    'CI/CD', 'POS Tagging', 'Azure', 'Time Series Analysis', 'Agile Methodology', 'Failover Systems', 'LightGBM',
    'Internet of Things (IoT)', 'Bash', 'Swift', 'MapReduce', 'XGBoost', 'Cryptography', 'Embedded Systems', 'HTML',
    'GPU Programming', 'Minitab', 'Supervised Learning', 'Spacy', 'Plotly', 'MySQL', 'Kotlin', 'HTTP/HTTPS',
    'Long Short-Term Memory (LSTM)', 'SQLite', 'Zoom', 'GDPR', 'Containerization', 'Tableau', 'Model Serving',
    'Operating Systems', 'Artificial Intelligence', 'Stream Processing', 'Data Warehousing', 'Red Teaming',
    'Model Monitoring', 'Bootstrap', 'Feature Engineering', 'Compliance', 'Mockito', 'CSS', 'Topic Modeling',
    'Recommender Systems', 'N-grams', 'Hyperparameter Tuning', 'Machine Learning', 'Python', 'Terraform',
    'Incident Response', 'Performance Tuning', 'Regular Expressions', 'Data Security', 'Linux', 'Edge Computing',
    'OAuth', 'LSTM', 'Model Evaluation', 'Rust', 'CSS3', 'Computer Architecture', 'Redis', 'Computational Biology',
    'Angular', 'Slack', 'Data Structures', 'SQL Queries', 'HTML5', 'Stemming', 'Blockchain', 'Attention Mechanism',
    'API Development', 'Robotics', 'Kubernetes', 'Word2Vec', 'Web Development', 'Test Automation', 'Computer Vision',
    'Batch Processing', 'Docker', 'TypeScript', 'Node.js', 'RESTful Services', 'Selenium', 'Ethical Hacking', 'Redux',
    'AI/ML Model Deployment', 'MATLAB', 'Seaborn', 'Data Preprocessing', 'Looker', 'Leadership', 'System Scaling',
    'ETL', 'Sentiment Analysis', 'DataOps', 'Knowledge Sharing', 'Product Management', 'Spark', 'Git',
    'Threat Modeling', 'Text Mining', 'Problem Solving', 'Regression', 'Technical Documentation', 'Critical Thinking',
    'C++', 'Apache Kafka', 'MLOps', 'Load Balancing', 'Hadoop', 'Confluence', 'Trello', 'TF-IDF',
    'Named Entity Recognition', 'Software Design Patterns', 'Data Governance', 'PostgreSQL', 'Knowledge Graphs',
    'Cryptocurrency', 'PHP', 'AI Ethics', 'Test-Driven Development (TDD)', 'Shell', 'Threading', 'Consulting',
    'Recurrent Neural Networks (RNNs)', 'Smart Contracts', 'Explainable AI (XAI)', 'Java', 'Data Modeling', 'Chatbots',
    'NoSQL', 'Data Wrangling', 'React', 'Dart', 'Pytest', 'Serverless Computing',
    'Generative Adversarial Networks (GANs)', 'Real-time Data Processing', 'Deep Learning', 'REST APIs',
    'Microservices Architecture', 'TensorFlow', 'Bag of Words', 'Cassandra', 'Networking', 'Machine Learning Models',
    'JavaScript', 'Socket Programming', 'AWS', 'Unit Testing', 'Unsupervised Learning', 'Model Tuning',
    'Backend Development', 'Cross-validation', 'Google Cloud', 'Parallel Computing', 'ETL Pipelines', 'Scikit-learn',
    'C', 'IDS/IPS', 'Data Structures and Algorithms', 'Distributed Ledger Technology (DLT)', 'Ruby',
    'Convolutional Neural Networks (CNNs)', 'CI/CD Automation', 'BigQuery', 'Gensim', 'Microservices', 'Scala',
    'Natural Language Processing', 'Penetration Testing', 'Artificial General Intelligence (AGI)', 'Data Science',
    'TCP/IP', 'Encryption', 'Algorithms', 'Research', 'Data Cleaning', 'Oracle', 'SOC 2', 'Perl',
    'Reinforcement Learning', 'Network Security', 'Event-Driven Architecture', 'Data Engineering',
    'Semi-supervised Learning', 'Autoencoders', 'SSL/TLS', 'Task Management', 'Multi-Agent Systems',
    'Stakeholder Management', 'Cloud Platforms', 'Tailwind CSS', 'Teamwork', 'GraphQL', 'Malware Analysis', 'R',
    'Nginx', 'Text Classification', 'Tokenization', 'Innovation', 'Dialog Systems', 'Object Oriented Programming',
    'Big Data', 'Power BI', 'Distributed Systems', 'Ansible', 'Clustering', 'Domain-Driven Design',
    'Cross-functional Teams', 'Keras', 'Pandas', 'OpenMP', 'RNN', 'Project Management'
]

CS_Generic_List = [
    # Core CS & Engineering
    "Data Structures",
    "Algorithms",
    "Computer Networks",
    "Operating Systems",
    "Database Management Systems",
    "Distributed Systems",
    "Software Engineering",
    "Computer Architecture",
    "Parallel Computing",
    "Embedded Systems",
    "Digital Logic Design",
    "Compilers",
    "Cloud Computing",
    "High Performance Computing",
    "Windows",
    "MacOs",

    # AI, ML, NLP, and Data Science
    "Data Science",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Reinforcement Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Time Series Analysis",
    "Recommender Systems",
    "Anomaly Detection",
    "Predictive Modeling",
    "Statistical Modeling",

    # Data Engineering & Big Data
    "Data Engineering",
    "Data Warehousing",
    "Big Data Analytics",
    "Data Pipelines",
    "Stream Processing",
    "ETL",
    "Data Mining",
    "Data Governance",
    "Data Visualization",
    "Business Intelligence",

    # Programming & Development
    "Object Oriented Programming",
    "Functional Programming",
    "Web Development",
    "Mobile App Development",
    "Game Development",
    "API Development",
    "Scripting",
    "Software Testing",
    "DevOps",
    "Agile Development",
    "CI/CD",
    "Version Control",

    # Cybersecurity & Systems
    "Cybersecurity",
    "Information Security",
    "Cryptography",
    "Network Security",
    "Security Engineering",
    "System Administration",
    "Penetration Testing",

    # Theoretical CS & Math
    "Discrete Mathematics",
    "Linear Algebra",
    "Probability and Statistics",
    "Graph Theory",
    "Information Theory",
    "Optimization",
    "Numerical Methods",
    "Theoretical Computer Science",
    "Automata Theory",

    # Misc & Emerging Domains
    "Human-Computer Interaction",
    "Robotics",
    "Augmented Reality",
    "Virtual Reality",
    "Digital Signal Processing",
    "Bioinformatics",
    "Computational Linguistics",
    "Scientific Computing",
    "Blockchain",
    "Internet of Things"
]


CS_Skills_List = CS_Comprehensive_List + CS_Generic_List

class SkillsExtractor:

    @staticmethod
    def extract_skills_from_resume(text):
        skills = []

        # Search for skills in the resume text
        for skill in set(CS_Skills_List):
            pattern = r"\b{}\b".format(re.escape(skill))
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                skills.append(skill)

        return skills

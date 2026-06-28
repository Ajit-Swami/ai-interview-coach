```markdown
# 🎯 AI Interview Coach

> AI-powered Interview Coach built on AWS EC2 using Python Flask and Amazon Bedrock.

---

## 💡 What It Does
- 🎤 Generates real interview questions by job role
- 🤖 Evaluates your answer using Amazon Bedrock AI
- ⭐ Gives score out of 10
- ✅ Shows what was good in your answer
- ⚠️ Shows what to improve
- 💡 Provides better answer example
- 🔄 Try unlimited questions anytime

---

## 🏗️ Architecture
```
User (Browser) → AWS EC2 Flask App → Amazon Bedrock → Nova Lite AI → Response
```

---

## 🛠️ Tech Stack
| Technology | Purpose |
|------------|---------|
| Python Flask | Backend Web Framework |
| Amazon Bedrock | AI Model API |
| Amazon Nova Lite | AI Language Model |
| AWS EC2 Ubuntu 22.04 | Cloud Server |
| IAM Role | AWS Security |
| Boto3 | AWS Python SDK |
| HTML CSS JavaScript | Frontend |

---

## 💼 Job Roles Supported
- Software Developer
- Data Analyst
- Gen AI Engineer
- Cloud Engineer
- Cybersecurity Analyst
- DevOps Engineer

---

## 🚀 How to Run

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-interview-coach.git
cd ai-interview-coach
```

### 2. Install Dependencies
```bash
pip3 install flask boto3 --break-system-packages
```

### 3. Run App
```bash
python3 app.py
```

### 4. Open Browser
```
http://your-ec2-ip:5000
```

---

## ☁️ AWS Setup
- EC2 Instance (Ubuntu 22.04, t2.micro)
- IAM Role with AmazonBedrockFullAccess attached to EC2
- Port 5000 open in Security Group
- Amazon Nova Lite enabled in Bedrock Console

---

## 📁 Project Structure
```
ai-interview-coach/
├── app.py        # Main Flask application
├── README.md     # Project documentation
└── .gitignore    # Git ignore file
```

---

## 🎯 What I Learned
- Deploying Python web apps on AWS EC2
- Integrating Amazon Bedrock AI API
- AWS IAM Role based security
- Building REST APIs with Flask
- Cloud deployment and configuration

---

## 👨‍💻 Author
**Ajit Swami** - Gen AI Intern

---




✅ Done! 😄

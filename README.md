# 🎯 AI Interview Coach
AI-powered Interview Coach built on AWS EC2 using Python Flask and Amazon Bedrock.

## 💡 What It Does
- Generates real interview questions by job role
- Evaluates your answer using AI
- Gives score out of 10
- Shows what was good and what to improve
- Provides better answer example

## 🛠️ Tech Stack
- Python Flask
- Amazon Bedrock (Nova Lite Model)
- AWS EC2 (Ubuntu 22.04)
- HTML + CSS + JavaScript
- Boto3

## 💼 Job Roles Supported
- Software Developer
- Data Analyst
- Gen AI Engineer
- Cloud Engineer
- Cybersecurity Analyst
- DevOps Engineer

## 🚀 How to Run
pip3 install flask boto3 --break-system-packages
python3 app.py
http://your-ec2-ip:5000

## ☁️ AWS Setup
- EC2 Instance (Ubuntu 22.04, t2.micro)
- IAM Role with AmazonBedrockFullAccess
- Port 5000 open in Security Group
- Amazon Nova Lite enabled in Bedrock

## 👨‍💻 Author
Your Name - Gen AI Intern



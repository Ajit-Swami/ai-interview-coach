from flask import Flask, request, jsonify, render_template_string
import boto3
import json

app = Flask(__name__)

# Connect to Amazon Bedrock - Using Nova Lite (Free)
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Interview Coach</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: Arial, sans-serif;
            background: #f0f4f8;
            padding: 30px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2d3748;
            margin-bottom: 5px;
            font-size: 28px;
        }
        .subtitle {
            color: #718096;
            margin-bottom: 25px;
        }
        label {
            font-weight: bold;
            color: #2d3748;
            display: block;
            margin-bottom: 5px;
        }
        select {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            font-size: 16px;
            border-radius: 8px;
            border: 2px solid #e2e8f0;
            background: white;
        }
        textarea {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            font-size: 15px;
            border-radius: 8px;
            border: 2px solid #e2e8f0;
            resize: vertical;
        }
        .btn {
            width: 100%;
            padding: 14px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 15px;
        }
        .btn-blue {
            background: #4299e1;
            color: white;
        }
        .btn-blue:hover { background: #2b6cb0; }
        .btn-green {
            background: #48bb78;
            color: white;
        }
        .btn-green:hover { background: #38a169; }
        .question-box {
            background: #ebf8ff;
            border-left: 4px solid #4299e1;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 17px;
            color: #2d3748;
            display: none;
        }
        .loading {
            text-align: center;
            color: #4299e1;
            font-size: 18px;
            padding: 20px;
            display: none;
        }
        .result-box {
            display: none;
            margin-top: 20px;
        }
        .score-box {
            background: #f0fff4;
            border: 2px solid #48bb78;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .score-number {
            font-size: 48px;
            font-weight: bold;
            color: #38a169;
        }
        .score-label {
            color: #718096;
            font-size: 16px;
        }
        .feedback-section {
            background: #f7fafc;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #4299e1;
        }
        .feedback-section h3 {
            color: #2d3748;
            margin-bottom: 8px;
            font-size: 16px;
        }
        .feedback-section p {
            color: #4a5568;
            line-height: 1.6;
        }
        .good { border-left-color: #48bb78; }
        .improve { border-left-color: #ed8936; }
        .better { border-left-color: #667eea; }
        .divider {
            border: none;
            border-top: 2px solid #e2e8f0;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 AI Interview Coach</h1>
        <p class="subtitle">Practice interviews and get instant AI feedback!</p>

        <label>Select Job Role:</label>
        <select id="role">
            <option value="Software Developer">Software Developer</option>
            <option value="Data Analyst">Data Analyst</option>
            <option value="Gen AI Engineer">Gen AI Engineer</option>
            <option value="Cloud Engineer">Cloud Engineer</option>
            <option value="Cybersecurity Analyst">Cybersecurity Analyst</option>
            <option value="DevOps Engineer">DevOps Engineer</option>
        </select>

        <button class="btn btn-blue" onclick="getQuestion()">
            🎤 Get Interview Question
        </button>

        <div class="question-box" id="questionBox">
            <strong>📌 Question:</strong><br><br>
            <span id="questionText"></span>
        </div>

        <div id="answerSection" style="display:none">
            <hr class="divider">
            <label>Your Answer:</label>
            <textarea id="answer" rows="6"
                placeholder="Type your answer here... Take your time!">
            </textarea>

            <button class="btn btn-green" onclick="getFeedback()">
                📊 Get AI Feedback
            </button>
        </div>

        <div class="loading" id="loading">
            ⏳ AI is thinking... Please wait...
        </div>

        <div class="result-box" id="resultBox">
            <hr class="divider">
            <h2 style="color:#2d3748; margin-bottom:15px;">
                📊 Your Interview Feedback
            </h2>

            <div class="score-box">
                <div class="score-number" id="scoreNumber">0</div>
                <div class="score-label">out of 10</div>
            </div>

            <div class="feedback-section good">
                <h3>✅ What was Good:</h3>
                <p id="goodText"></p>
            </div>

            <div class="feedback-section improve">
                <h3>⚠️ What to Improve:</h3>
                <p id="improveText"></p>
            </div>

            <div class="feedback-section better">
                <h3>💡 Better Answer Example:</h3>
                <p id="betterText"></p>
            </div>

            <hr class="divider">
            <button class="btn btn-blue" onclick="resetApp()">
                🔄 Try Another Question
            </button>
        </div>
    </div>

    <script>
        let currentQuestion = "";

        function showLoading() {
            document.getElementById("loading").style.display = "block";
            document.getElementById("resultBox").style.display = "none";
        }

        function hideLoading() {
            document.getElementById("loading").style.display = "none";
        }

        function resetApp() {
            document.getElementById("questionBox").style.display = "none";
            document.getElementById("answerSection").style.display = "none";
            document.getElementById("resultBox").style.display = "none";
            document.getElementById("answer").value = "";
            currentQuestion = "";
        }

        async function getQuestion() {
            const role = document.getElementById("role").value;
            resetApp();
            showLoading();

            try {
                const res = await fetch("/get-question", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({role: role})
                });
                const data = await res.json();

                if (data.error) {
                    alert("Error: " + data.error);
                    hideLoading();
                    return;
                }

                currentQuestion = data.question;
                document.getElementById("questionText").innerText = data.question;
                document.getElementById("questionBox").style.display = "block";
                document.getElementById("answerSection").style.display = "block";
                hideLoading();

            } catch(err) {
                alert("Something went wrong! Check terminal for error.");
                hideLoading();
            }
        }

        async function getFeedback() {
            const answer = document.getElementById("answer").value.trim();
            const role = document.getElementById("role").value;

            if (!answer) {
                alert("Please type your answer first!");
                return;
            }

            showLoading();

            try {
                const res = await fetch("/get-feedback", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        role: role,
                        question: currentQuestion,
                        answer: answer
                    })
                });
                const data = await res.json();

                if (data.error) {
                    alert("Error: " + data.error);
                    hideLoading();
                    return;
                }

                document.getElementById("scoreNumber").innerText = data.score;
                document.getElementById("goodText").innerText = data.good;
                document.getElementById("improveText").innerText = data.improve;
                document.getElementById("betterText").innerText = data.better;
                document.getElementById("resultBox").style.display = "block";
                hideLoading();

            } catch(err) {
                alert("Something went wrong! Check terminal for error.");
                hideLoading();
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/get-question", methods=["POST"])
def get_question():
    try:
        role = request.json.get("role")

        prompt = f"""You are an expert interviewer.
Generate ONE real interview question for a {role} position.
Only give the question, nothing else. No extra text."""

        response = bedrock.invoke_model(
            modelId="us.amazon.nova-lite-v1:0",
            body=json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ]
            })
        )

        result = json.loads(response['body'].read())
        question = result['output']['message']['content'][0]['text']
        return jsonify({"question": question})

    except Exception as e:
        print(f"Error in get_question: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/get-feedback", methods=["POST"])
def get_feedback():
    try:
        data = request.json
        role = data.get("role")
        question = data.get("question")
        answer = data.get("answer")

        prompt = f"""You are an expert interview coach for {role} role.

Interview Question: {question}
Candidate Answer: {answer}

Evaluate the answer and respond in this EXACT JSON format:
{{
  "score": <number between 1 to 10>,
  "good": "<what was good in the answer in 2-3 lines>",
  "improve": "<what needs improvement in 2-3 lines>",
  "better": "<write a better sample answer in 3-4 lines>"
}}

Respond with JSON only. No extra text before or after."""

        response = bedrock.invoke_model(
            modelId="us.amazon.nova-lite-v1:0",
            body=json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ]
            })
        )

        result = json.loads(response['body'].read())
        feedback_text = result['output']['message']['content'][0]['text']

        # Clean response if needed
        feedback_text = feedback_text.strip()
        if feedback_text.startswith("```"):
            feedback_text = feedback_text.split("```")[1]
            if feedback_text.startswith("json"):
                feedback_text = feedback_text[4:]

        feedback = json.loads(feedback_text)
        return jsonify(feedback)

    except Exception as e:
        print(f"Error in get_feedback: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
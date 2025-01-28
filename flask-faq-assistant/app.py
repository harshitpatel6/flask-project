from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
import openai
import os
from datetime import datetime
from markdown2 import markdown

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure OpenAI and MongoDB
openai.api_key = os.getenv('OPENAI_API_KEY')
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client.faq_assistant

# Load the knowledge base
def load_knowledge_base():
    with open("knowledge_base/knowledge.md", "r") as file:
        return markdown(file.read())

# Query OpenAI LLM
def query_llm(user_query, knowledge_base):
    prompt = f"Answer the query based on the provided knowledge base:\n\nKnowledge Base:\n{knowledge_base}\n\nQuery: {user_query}\n"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        user_query = request.form['query']
        knowledge_base = load_knowledge_base()
        response = query_llm(user_query, knowledge_base)

        # Log the interaction
        db.logs.insert_one({
            "query": user_query,
            "response": response,
            "timestamp": datetime.now()
        })

    return render_template("index.html", response=response)

@app.route("/ask", methods=["POST"])
def api_ask():
    data = request.json
    user_query = data.get("query")
    knowledge_base = load_knowledge_base()
    response = query_llm(user_query, knowledge_base)

    # Log the interaction
    db.logs.insert_one({
        "query": user_query,
        "response": response,
        "timestamp": datetime.now()
    })

    return jsonify({"response": response})

@app.route("/view-logs", methods=["GET"])
def view_logs():
    logs = list(db.logs.find({}, {"_id": 0}))
    return jsonify(logs)

@app.route("/update-knowledge", methods=["POST"])
def update_knowledge():
    file = request.files['file']
    file.save("knowledge_base/knowledge.md")
    return "Knowledge base updated successfully!"

if __name__ == "__main__":
    app.run(debug=True)

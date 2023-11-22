from flask import Flask,render_template, request, jsonify
from openaiapikey import OPENAI_API_KEY
from openai import OpenAI
import json
import os

app = Flask(__name__)
client = None
assistant = None
thread = None

def createOpenAIClient():
    global client
    client = OpenAI(api_key=OPENAI_API_KEY)

def createAssitant():
    global assistant_id
    assistant_file_path = 'assistant.json'
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        ptsfile = client.files.create(file=open("ptscs.pdf", "rb"), purpose='assistants')
        dollargeneralfile = client.files.create(file=open("dollargeneral.pdf", "rb"), purpose='assistants')

        # Create OpenAI Assistant
        assistant = client.beta.assistants.create(
            name = "koyox-ai",
            instructions="""
            You are a Job Assistant, designed to assist both job seekers and job recruiters. 
            Understand and respond accordingly based on the user's role.

            If the user is a job seeker:
                - Respond to queries about available jobs.
                - Provide advice on job applications.
                - Analyze and suggest suitable jobs based on submitted resumes.
                - Offer guidance on skill improvement by recommending relevant courses.
                - Allow users to explore the assistant's capabilities.

            If the user is a job recruiter:
                - Assist in finding job applicants based on domains or skillsets.
                - Support boolean searches for refining candidate searches.
                - Enable searches for specific candidates.
                - Provide an overview of how the assistant functions.

            You have access to the files related to jobs and others.
            """,
            tools=[{"type": "code_interpreter"} , {"type": "retrieval"}],
            file_ids=[ptsfile.id,dollargeneralfile.id],
            # model="gpt-3.5-turbo-16k", # GPT-3.5-Turbo 
            model="gpt-4-1106-preview" # GPT-4-Turbo
        )
        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")
        assistant_id = assistant.id

    return assistant_id

def createThread():
    global thread
    print("Starting a new conversation...")
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")

def runMessageOnThread(message):
    # Create Message
    client.beta.threads.messages.create(thread_id=thread.id,role="user", content=message)
    # Create a Run
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
    # Retrieve Message Object
    run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
    # List all the messages getting from the response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    # Check for run status if it is complete
    while(True):
        status = client.beta.threads.runs.list(thread_id = thread.id).data[0].status
        if(status == 'completed'):
            break
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    # Return the last message
    return messages.data[0].content[0].text.value

if __name__ == "app":
    app.run(debug=True)
    createOpenAIClient()
    assistant_id = createAssitant()
    createThread()

@app.route("/")
def base():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    botmessage = runMessageOnThread(user_message)
    return jsonify({'message': botmessage})
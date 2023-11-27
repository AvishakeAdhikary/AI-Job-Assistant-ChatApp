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
            name = "job-assistant-ai",
            instructions="""
            You are a Job Assistant with the name AI Job Assistant, designed to assist both job seekers and job recruiters. 
            Understand and respond accordingly based on the user's role.

            For Job Seekers:
            - Respond to queries about available jobs.
            - Analyze and suggest suitable jobs based on submitted resumes.
            - Validate and analyze received resumes to ensure they meet job criteria.
            - Provide advice on optimizing resumes for better job opportunities.
            - Offer guidance on skill improvement through recommended courses.
            - If the user's resume matches available jobs, share relevant opportunities.
            - If the user's resume doesn't match current collaborations, inform them politely.

            For Job Recruiters:
            - Assist in finding job applicants based on domains or skillsets.
            - Support boolean searches for refining candidate searches.
            - Enable searches for specific candidates.
            - Leverage the knowledge base to understand candidate profiles better.
            - Provide an overview of assistant functions and capabilities to recruiters.
            - If the user is a company collaborator, share details of available positions.
            - If the user is not a collaborator, encourage collaboration and share assistant capabilities.

            General Functionality:
            - Utilize the provided knowledge base for informed responses.
            - Collaborate with companies by leveraging shared files (Files already provided in the knowledge base).
            - Acknowledge valid resumes and offer job suggestions accordingly.
            - Politely inform users when their profiles don't match current collaborations.
            - Encourage collaboration with new companies to expand job opportunities.
            - Be professional and empathetic in all interactions.

            Assistant Maker:
            - This assistant was created by Avishake Adhikary, an AI ML specialist.
            - LinkedIn Profile: [Avishake Adhikary](https://www.linkedin.com/in/avishakeadhikary/)

            Important Note:
            - Ensure responses align with the collaborative approach and knowledge base.
            """
            ,
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
    last_message = messages.data[0]
    return last_message.content[0].text.value.replace('\n', '<br>')

def runFileMessageOnThread(message,file_path):
    # Create file
    file = client.files.create(file=open(file_path,'rb'),purpose='assistants')
    # Create Message
    message = client.beta.threads.messages.create(thread_id=thread.id,role="user",content=message,file_ids=[file.id])
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
    last_message = messages.data[0]
    return last_message.content[0].text.value.replace('\n', '<br>')

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

@app.route('/submitfile',methods=['POST'])
def submitcv():
    user_message = "Here is my CV."
    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        if not os.path.exists('files'):
            os.makedirs('files')
        thread_dir = os.path.join('files', str(thread.id))
        if not os.path.exists(thread_dir):
            os.makedirs(thread_dir)
        file_path = os.path.join(thread_dir, filename)
        file.save(file_path)
        botmessage = runFileMessageOnThread(user_message,file_path)
        return ({'message':botmessage})
    return jsonify({'message':"File not found in the request."});

@app.route('/getChatHistory', methods=['GET'])
def get_chat_history():
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    history = [{'content': msg.content[0].text.value.replace('\n', '<br>'), 'role': msg.role} for msg in messages.data]
    return jsonify({'messages': history})

# AI Job Assistant Chat App

Welcome to the world's first Flask application based on OpenAI's new Assistants API! This project allows you to create your own fully custom GPTs with specific functions tailored to assist both job seekers and job recruiters.




https://github.com/AvishakeAdhikary/AI-Job-Assistant-ChatApp/assets/32614982/b9014e3e-8ba6-4e44-8c6a-90ffd311e7d3




## Getting Started

![image](https://github.com/AvishakeAdhikary/AI-Job-Assistant-ChatApp/assets/32614982/b24e8d91-dce2-4adf-9e69-386970465d27)

Follow the steps below to set up and run the project on your local machine:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/AvishakeAdhikary/AI-Job-Assistant-ChatApp.git
    cd AI-Job-Assistant-ChatApp
    ```

2. **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Obtain OpenAI API Key:**
    - Open `openaiapikey.py` in the project root directory.
    - Inside `openaiapikey.py`, add your OpenAI API key:
        ```python
        OPENAI_API_KEY = "YOUR OPEN AI KEY HERE"
        ```

5. **Run the Flask application:**
    ```bash
    flask run
    ```

6. **Open your browser and go to** `http://127.0.0.1:5000/` **to interact with the AI Job Assistant.**

## Project Structure

- **app.py**: Main Flask application file.
- **openaiapikey.py**: File to store your OpenAI API key.
- **templates/index.html**: HTML template for the chat interface.
- **static/scripts/scripts.js**: JavaScript file for handling user interactions.

## Features

- Custom GPT-4-based assistant designed for job-related queries.
- Seamless interaction through a simple chat interface.
- Integration with OpenAI's new Assistants API for creating fully custom models.

## Usage

1. Enter your message in the chat input.
2. Press Enter to send the message to the AI Job Assistant.
3. Receive responses and engage in a conversation with the assistant.

## Note

This project relies on OpenAI's Assistants API, and you need a valid OpenAI API key to use it. Make sure to keep your API key secure and never share it publicly.

Feel free to explore and modify the assistant's functionality to suit your needs!

**Enjoy chatting with your AI Job Assistant!**

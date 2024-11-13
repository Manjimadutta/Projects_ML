import os
import requests
from dotenv import load_dotenv

rapidai_KEY = os.getenv('rapidai_KEY')


## Step 1: Defining the API endpoint (picked up from RapidAPI platform )
url = "https://chatgpt-best-price.p.rapidapi.com/v1/chat/completions"

# Step 2: Defining the headers with user obtained API key from rapidAPI website
headers = {
    "x-rapidapi-key": rapidai_KEY,
    "x-rapidapi-host": "chatgpt-best-price.p.rapidapi.com",
    "Content-Type": "application/json"
}

# Step 3 : Write function to take questions as argumet from user
def ask_question():
    # Take input from the user (question)
    user_question = input("Ask me anything: ")

    # Prepare the payload with the user's question
    payload = {
        "model": "gpt-4o-mini", 
        "messages": [
            {
                "role": "user",
                "content": user_question  
            }
        ]
    }

    # Step 4 : Sending the request to the API with required parameters
    response = requests.post(url, json=payload, headers=headers)

    # Step 5 : Parsing the response and extract the answer
    response_data = response.json()

    # Step 6 : Extract just the answer from the response
    answer = response_data['choices'][0]['message']['content']

    print("\nAnswer:", answer)

# Run the function to start the chatbot and receive question from users
ask_question()
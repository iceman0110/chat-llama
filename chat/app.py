import requests

url = "http://127.0.0.1:8002/chat"  # Corrected endpoint

def main():
    while True:
        # Get user input
        user_input = input("User: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting the chatbot. Goodbye!")
            break

        # Send the user input to the API
        response = requests.post(url=url, json={"question": user_input})

        # Check if the response is successful
        if response.status_code == 200:
            chatbot_response = response.json().get("response", "No response received")
            print(f"Chatbot: {chatbot_response}")
        else:
            print(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")

if __name__ == "__main__":
    main()

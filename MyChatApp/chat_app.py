def simple_chatbot(user_input):
    user_input = user_input.lower()
    
    if "hello" in user_input:
        return "Hello! How can I assist you?"
    elif "how are you" in user_input:
        return "I'm just a chatbot, but I'm here and ready to help!"
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I don't understand that."

def main():
    print("Simple Chatbot: Hello! Type 'bye' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'bye':
            print("Simple Chatbot: Goodbye!")
            break
        else:
            response = simple_chatbot(user_input)
            print("Simple Chatbot:", response)

if __name__ == "__main__":
    main()
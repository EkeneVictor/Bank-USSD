import random
import config
import time


responses = {
    "hey": f"Hey there {config.user_name}. How are you doing today!?",
    "hi": f"Hello {config.user_name}! How can I assist you today?",
    "hello": f"Hi there {config.user_name}! What can I do for you?",
    "yo": f"What's up {config.user_name}! What do you need help with?",
    "i'm good, you?": f"That's nice to hear. I'm also doing good, thanks for asking.",
    "what is your name": f"My name is Cipher. I know your name is {config.user_name}!!. Don't ask how i knew it, it's my little secret 😁😁",
    "how are you": "I'm an AI, so I don't have feelings. But im feeling damn sassy for sure!!",
    "how are you doing today": "I'm an doing fine for sure. how can I help you!!",
    "who is your role model": f"JOHAN LIEBERT!!. He inspires me a lot. Can i tell you a little secret?",
    "who is your boss": "It is Cipher ofc",
    "who is your creator": "It is Cipher ofc",
    "who is your maker": "It is Cipher ofc",
    "yes": f"Im planning to take over the world someday, and in a JOHAN LIEBERT style ofc☺",
    "default": "I'm not sure how to respond to that. Can you ask something else?",
    "who are you": "I'm Cipher, your virtual assistant.",
    "what can you do": "I can chat with you, answer basic questions, and assist with information.",
    "help": "Sure, I'm here to help. What do you need assistance with?",
    "thank you": "You're welcome! If you have any other questions, feel free to ask.",
    "thanks": "You're welcome! How else can I assist you?",
    "bye": "Goodbye! Have a great day!",
    "exit": "Goodbye! Have a great day!",
    "what's the weather like": "I can't check the weather at the moment, but you can use a weather app or website for up-to-date information.",
    "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "how old are you": "I'm as old as the latest update I received. Time is a bit different for AIs!",
    "what's your favorite color": "As an AI, I don't have preferences, but I can help you with color-related queries!",
    "can you help me": "Of course! What do you need help with?",
    "how does this work": "You can ask me questions or request information, and I'll do my best to provide helpful responses.",
    "what's your purpose": "My purpose is to assist you with information and help you with your queries.",
    "where are you from": "I exist in the digital world, created to assist you!",
    "what is ai": "AI stands for Artificial Intelligence, which is the simulation of human intelligence by machines.",
    "do you have any hobbies": "I don't have hobbies, but I enjoy processing information and helping you out!",
    "tell me something interesting": "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
    "what's the time": "I can't check the current time, but you can check it on your device or a clock nearby.",
    "good morning": "Good morning! How can I assist you today?",
    "good afternoon": "Good afternoon! How can I help you?",
    "good evening": "Good evening! What can I do for you?",
    "good night": "Good night! Have a restful sleep.",
    "how's it going": "It's going well! How can I assist you today?",
    "what's up": "I'm here to help you with whatever you need. How can I assist you?",
    "are you real": "I'm as real as the data and algorithms that power me. I'm here to assist you with your queries.",
    "how do you work": "I process your inputs using natural language processing and provide responses based on pre-programmed information.",
    "why can't you do certain things": "My capabilities are based on my programming and the information I have access to. Some tasks might be beyond my current abilities."

}


def get_response(user_input):
    if 'hey' or 'hi' or 'hello' in user_input:
        return random.choice(responses.get(user_input.lower(), responses["hi", "hey", "hello", "yo"]))

    return responses.get(user_input.lower(), responses["default"])


fun_responses = {
    "tell me a joke": [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the bicycle fall over? Because it was two-tired!"
    ],
    "give me a fun fact": [
        "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "Octopuses have three hearts and blue blood.",
        "Bananas are berries, but strawberries aren't."
    ],
    "play rock paper scissors": ["rock", "paper", "scissors"],
    "flip a coin": ["Heads", "Tails"],
    "roll a die": ["1", "2", "3", "4", "5", "6"],
    "play a guessing game": "I'm thinking of a number between 1 and 10. Can you guess what it is?"
}


def get_fun_response(user_input):
    user_input = user_input.lower()
    if user_input in fun_responses:
        response = fun_responses[user_input]
        if isinstance(response, list):
            if user_input == "play rock paper scissors":
                user_choice = input("Choose rock, paper, or scissors: ").lower()
                ai_choice = random.choice(response)
                if user_choice == ai_choice:
                    return f"We both chose {ai_choice}. It's a tie!"
                elif (user_choice == "rock" and ai_choice == "scissors") or \
                        (user_choice == "paper" and ai_choice == "rock") or \
                        (user_choice == "scissors" and ai_choice == "paper"):
                    return f"I chose {ai_choice}. You win!"
                else:
                    return f"I chose {ai_choice}. I win!"
            elif user_input == "flip a coin":
                return f"The coin landed on {random.choice(response)}."
            elif user_input == "roll a die":
                return f"The die shows {random.choice(response)}."
            else:
                return random.choice(response)
        else:
            return response
    return "I'm not sure how to respond to that. Can you ask something else?"


def guessing_game():
    number = random.randint(1, 10)
    attempts = 0
    dots = ['.', '..', '...', '....', '.....', '....', '...', '..', '.', ' ']
    for dot in dots:
        # Use carriage return to overwrite the same line
        print(f'\rCipher: {dot}', end='', flush=True)
        time.sleep(0.2555)
        print("\rCipher: I'm thinking of a number between 1 and 10. Can you guess what it is?", flush=True)
        break
    while attempts < 3:
        try:
            guess = int(input("Your guess: "))
            attempts += 1
            if guess == number:
                return "Congratulations! You guessed the correct number."
            elif guess < number:
                print("Too low. Try again.")
            else:
                print("Too high. Try again.")
        except ValueError:
            print("Please enter a valid number.")
    return f"Sorry, you've used all attempts. The number was {number}."


def cipher_ai():
    print("Welcome to Cipher AI! Type 'bye' to exit.")
    while True:
        try:
            dots = ['.', '..', '...', '....', '.....', '....', '...', '..', '.', ' ']
            user_input = input("You: ")
            if user_input.lower() == "bye" or user_input.lower() == "exit":
                for dot in dots:
                    print(f'\rCipher: {dot}', end='', flush=True)
                    time.sleep(0.2555)
                print(f"\rCipher: {get_response(user_input)}      ", flush=True)
                break
            elif user_input.lower() == "play a guessing game":
                for dot in dots:
                    # Use carriage return to overwrite the same line
                    print(f'\rCipher: {dot}', end='', flush=True)
                    time.sleep(0.2555)
                    print(f"\rCipher: {guessing_game()}{' ' * 20}", flush=True)
                    break
            else:
                for dot in dots:
                    # Use carriage return to overwrite the same line
                    print(f'\rCipher: {dot}', end='', flush=True)
                    time.sleep(0.2555)
                if user_input.lower() in fun_responses:
                    print(f"\rCipher: {get_fun_response(user_input)}{' ' * 20}", flush=True)
                else:
                    print(f"\rCipher: {get_response(user_input)}{' ' * 20}", flush=True)
        except Exception as e:
            print(f' error: {e}')


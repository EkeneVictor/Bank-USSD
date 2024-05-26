import random
from utilities import typing_dots, print_slowly


# Function for the "Guess the Number" game
def play_guess_number():
    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        guess = input("Your guess: ")
        attempts += 1

        try:
            guess = int(guess)
        except ValueError:
            bot_response = "Please enter a valid number."
            typing_dots()
            print_slowly(bot_response + '\n')
            continue

        if guess < secret_number:
            bot_response = "Too low! Try again."
            typing_dots()
            print_slowly(bot_response + '\n')
        elif guess > secret_number:
            bot_response = "Too high! Try again."
            typing_dots()
            print_slowly(bot_response + '\n')
        else:
            bot_response = f"Congratulations! You guessed the number in {attempts} attempts."
            typing_dots()
            print_slowly(bot_response + '\n')
            break


# Function to play the Word Association Game
def play_word_association():
    word_list = ["apple", "banana", "carrot", "dog", "elephant", "football", "guitar", "house", "ice cream", "jungle"]

    bot_response = "Welcome to the Word Association Game!"
    typing_dots()
    print_slowly(bot_response + '\n')
    bot_response = "I'll say a word, and you have to respond with the first word that comes to your mind."
    typing_dots()
    print_slowly(bot_response + '\n')
    bot_response = "Let's begin!"
    typing_dots()
    print_slowly(bot_response + '\n')
    score = 0

    # Game loop
    while True:
        # Choose a random word from the word list
        word = random.choice(word_list)
        bot_response = word.capitalize()
        typing_dots()
        print_slowly(bot_response + '\n')

        # Get user's response
        user_input = input("You: ").lower()

        # Check if the user's response matches the first letter of the word
        if user_input.startswith(word[0]):
            bot_response = "Correct!"
            typing_dots()
            print_slowly(bot_response + '\n')
            score += 1
        else:
            bot_response = f"Incorrect! The word should start with '{word[0]}'."
            typing_dots()
            print_slowly(bot_response + '\n')

        # Ask if the user wants to continue playing
        bot_response = "Do you want to continue?; (yes/no):"
        typing_dots()
        print_slowly(bot_response + '\n')
        play_again = input("You: ").lower()
        if play_again != 'yes':
            break

    # Display final score
    bot_response = f"Your final score is: {score}"
    typing_dots()
    print_slowly(bot_response + '\n')


def play_trivia_quiz():
    bot_response = "Welcome to the Trivia Quiz!"
    typing_dots()
    print_slowly(bot_response + '\n')
    bot_response = "I'll ask you some questions, and you have to choose the correct answer."
    typing_dots()
    print_slowly(bot_response + '\n')
    bot_response = "Let's begin!"
    typing_dots()
    print_slowly(bot_response + '\n')
    score = 0

    # Define a list of trivia questions and answers
    questions = [
        {
            "question": "What is the capital of France?",
            "options": ["A. Berlin", "B. Madrid", "C. Paris", "D. Rome"],
            "answer": "C"
        },
        {
            "question": "Who wrote 'To Kill a Mockingbird'?",
            "options": ["A. Harper Lee", "B. Mark Twain", "C. J.K. Rowling", "D. Ernest Hemingway"],
            "answer": "A"
        },
        {
            "question": "What is the smallest planet in our solar system?",
            "options": ["A. Earth", "B. Mars", "C. Mercury", "D. Venus"],
            "answer": "C"
        },
        # Add more questions as needed
    ]

    # Game loop
    for q in questions:
        bot_response = q["question"]
        typing_dots()
        print_slowly(bot_response + '\n')
        # print(q["question"])
        for option in q["options"]:
            bot_response = option
            typing_dots()
            print_slowly(bot_response + '\n')
            # print(option)

        user_input = input("Your answer: ").upper()

        if user_input == q["answer"]:
            bot_response = "Correct"
            typing_dots()
            print_slowly(bot_response + '\n')
            score += 1
        elif user_input == 'exit':
            bot_response = 'You have exited the trivia'
            typing_dots()
            print_slowly(bot_response + '\n')
            bot_response = f"Your final score is: {score}"
            typing_dots()
            print_slowly(bot_response + '\n')
            break
        else:
            bot_response = f"Incorrect! The correct answer was '{q["answer"]}'."
            typing_dots()
            print_slowly(bot_response + '\n')

    # Display final score
    bot_response = f"Your final score is: {score}"
    typing_dots()
    print_slowly(bot_response + '\n')

import random
from utilities import typing_dots, print_slowly


# Function for the "Guess the Number" game
def play_guess_number():
    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        guess = input("You: ")
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

        # statement that lets the user stop the game
        if user_input == 'stop':
            break

    # Display final score
    bot_response = f"Your final score is: {score}"
    typing_dots()
    print_slowly(bot_response + '\n')

    if score < 50:
        bot_response = f"You're pretty dumb, no offense😂😂"
        typing_dots()
        print_slowly(bot_response + '\n')
    else:
        bot_response = f"Congrats, you're smarter than most"
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
            "options": ["A) London", "B) Berlin", "C) Paris", "D) Madrid"],
            "answer": "C"
        },
        {
            "question": "What is 2 + 2?",
            "options": ["A) 3", "B) 4", "C) 5", "D) 6"],
            "answer": "B"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["A) Earth", "B) Mars", "C) Jupiter", "D) Saturn"],
            "answer": "B"
        },
        {
            "question": "Who wrote 'To Kill a Mockingbird'?",
            "options": ["A) Harper Lee", "B) Jane Austen", "C) J.K. Rowling", "D) Mark Twain"],
            "answer": "A"
        },
        {
            "question": "What is the largest ocean on Earth?",
            "options": ["A) Atlantic", "B) Indian", "C) Arctic", "D) Pacific"],
            "answer": "D"
        },
        {
            "question": "In which year did the Titanic sink?",
            "options": ["A) 1912", "B) 1905", "C) 1898", "D) 1923"],
            "answer": "A"
        },
        {
            "question": "What is the chemical symbol for Gold?",
            "options": ["A) Au", "B) Ag", "C) Fe", "D) Hg"],
            "answer": "A"
        },
        {
            "question": "Which country is known as the Land of the Rising Sun?",
            "options": ["A) China", "B) Japan", "C) Thailand", "D) South Korea"],
            "answer": "B"
        },
        {
            "question": "Who painted the Mona Lisa?",
            "options": ["A) Vincent van Gogh", "B) Pablo Picasso", "C) Leonardo da Vinci", "D) Claude Monet"],
            "answer": "C"
        },
        {
            "question": "What is the largest mammal in the world?",
            "options": ["A) Elephant", "B) Blue Whale", "C) Giraffe", "D) Great White Shark"],
            "answer": "B"
        },
        {
            "question": "Which planet is closest to the sun?",
            "options": ["A) Venus", "B) Earth", "C) Mercury", "D) Mars"],
            "answer": "C"
        },
        {
            "question": "What is the hardest natural substance on Earth?",
            "options": ["A) Gold", "B) Iron", "C) Diamond", "D) Silver"],
            "answer": "C"
        },
        {
            "question": "Who is known as the Father of Computers?",
            "options": ["A) Charles Babbage", "B) Alan Turing", "C) Bill Gates", "D) Steve Jobs"],
            "answer": "A"
        },
        {
            "question": "Which element has the chemical symbol O?",
            "options": ["A) Gold", "B) Oxygen", "C) Hydrogen", "D) Helium"],
            "answer": "B"
        },
        {
            "question": "What is the longest river in the world?",
            "options": ["A) Amazon", "B) Nile", "C) Yangtze", "D) Mississippi"],
            "answer": "B"
        },
        {
            "question": "In which year did World War II end?",
            "options": ["A) 1942", "B) 1945", "C) 1950", "D) 1955"],
            "answer": "B"
        },
        {
            "question": "What is the capital of Australia?",
            "options": ["A) Sydney", "B) Melbourne", "C) Canberra", "D) Brisbane"],
            "answer": "C"
        },
        {
            "question": "Who invented the telephone?",
            "options": ["A) Alexander Graham Bell", "B) Thomas Edison", "C) Nikola Tesla", "D) Guglielmo Marconi"],
            "answer": "A"
        },
        {
            "question": "What is the square root of 64?",
            "options": ["A) 6", "B) 7", "C) 8", "D) 9"],
            "answer": "C"
        },
        {
            "question": "Which gas is most abundant in the Earth's atmosphere?",
            "options": ["A) Oxygen", "B) Carbon Dioxide", "C) Nitrogen", "D) Hydrogen"],
            "answer": "C"
        },
        {
            "question": "What is the smallest country in the world?",
            "options": ["A) Monaco", "B) San Marino", "C) Vatican City", "D) Liechtenstein"],
            "answer": "C"
        },
        {
            "question": "Who wrote 'Pride and Prejudice'?",
            "options": ["A) Emily Brontë", "B) Jane Austen", "C) Charles Dickens", "D) George Orwell"],
            "answer": "B"
        },
        {
            "question": "What is the tallest mountain in the world?",
            "options": ["A) K2", "B) Kangchenjunga", "C) Mount Everest", "D) Lhotse"],
            "answer": "C"
        },
        {
            "question": "In which city is the Statue of Liberty located?",
            "options": ["A) Boston", "B) Philadelphia", "C) New York City", "D) Washington D.C."],
            "answer": "C"
        },
        {
            "question": "Who developed the theory of relativity?",
            "options": ["A) Isaac Newton", "B) Albert Einstein", "C) Niels Bohr", "D) Galileo Galilei"],
            "answer": "B"
        },
        {
            "question": "Which country hosted the 2016 Summer Olympics?",
            "options": ["A) China", "B) Brazil", "C) UK", "D) Japan"],
            "answer": "B"
        },
        {
            "question": "What is the chemical symbol for water?",
            "options": ["A) H2O", "B) CO2", "C) O2", "D) H2"],
            "answer": "A"
        },
        {
            "question": "Who is the author of 'Harry Potter' series?",
            "options": ["A) J.R.R. Tolkien", "B) J.K. Rowling", "C) George R.R. Martin", "D) Stephen King"],
            "answer": "B"
        },
        {
            "question": "Which planet is known as the Earth's twin?",
            "options": ["A) Mars", "B) Venus", "C) Jupiter", "D) Saturn"],
            "answer": "B"
        },
        {
            "question": "What is the main ingredient in guacamole?",
            "options": ["A) Tomato", "B) Onion", "C) Avocado", "D) Lemon"],
            "answer": "C"
        },
        {
            "question": "Which element has the chemical symbol Na?",
            "options": ["A) Nitrogen", "B) Sodium", "C) Neon", "D) Nickel"],
            "answer": "B"
        },
        {
            "question": "What is the largest planet in our solar system?",
            "options": ["A) Earth", "B) Jupiter", "C) Saturn", "D) Neptune"],
            "answer": "B"
        },
        {
            "question": "Who painted the ceiling of the Sistine Chapel?",
            "options": ["A) Leonardo da Vinci", "B) Michelangelo", "C) Raphael", "D) Donatello"],
            "answer": "B"
        },
        {
            "question": "Which country is home to the kangaroo?",
            "options": ["A) New Zealand", "B) Australia", "C) South Africa", "D) India"],
            "answer": "B"
        },
        {
            "question": "What is the capital of Italy?",
            "options": ["A) Milan", "B) Rome", "C) Florence", "D) Venice"],
            "answer": "B"
        },
        {
            "question": "What is the fastest land animal?",
            "options": ["A) Cheetah", "B) Lion", "C) Gazelle", "D) Horse"],
            "answer": "A"
        },
        {
            "question": "What is the boiling point of water at sea level in Celsius?",
            "options": ["A) 50°C", "B) 75°C", "C) 100°C", "D) 125°C"],
            "answer": "C"
        },
        {
            "question": "Which city is known as the Big Apple?",
            "options": ["A) Los Angeles", "B) Chicago", "C) New York City", "D) San Francisco"],
            "answer": "C"
        },
        {
            "question": "Who was the first person to walk on the moon?",
            "options": ["A) Yuri Gagarin", "B) Neil Armstrong", "C) Buzz Aldrin", "D) Michael Collins"],
            "answer": "B"
        },
        {
            "question": "What is the main language spoken in Brazil?",
            "options": ["A) Spanish", "B) English", "C) Portuguese", "D) French"],
            "answer": "C"
        },
        {
            "question": "Which gas do plants absorb from the atmosphere?",
            "options": ["A) Oxygen", "B) Carbon Dioxide", "C) Nitrogen", "D) Hydrogen"],
            "answer": "B"
        },
        {
            "question": "Who wrote 'The Great Gatsby'?",
            "options": ["A) Ernest Hemingway", "B) F. Scott Fitzgerald", "C) William Faulkner", "D) John Steinbeck"],
            "answer": "B"
        },
        {
            "question": "What is the largest desert in the world?",
            "options": ["A) Sahara", "B) Arabian", "C) Gobi", "D) Antarctic"],
            "answer": "D"
        },
        {
            "question": "Which country is the largest by land area?",
            "options": ["A) Canada", "B) China", "C) USA", "D) Russia"],
            "answer": "D"
        },
        {
            "question": "What is the smallest prime number?",
            "options": ["A) 0", "B) 1", "C) 2", "D) 3"],
            "answer": "C"
        },
        {
            "question": "Who discovered penicillin?",
            "options": ["A) Alexander Fleming", "B) Louis Pasteur", "C) Marie Curie", "D) Isaac Newton"],
            "answer": "A"
        },
        {
            "question": "What is the currency of Japan?",
            "options": ["A) Yuan", "B) Yen", "C) Won", "D) Dollar"],
            "answer": "B"
        },
        {
            "question": "Which continent is known as the Dark Continent?",
            "options": ["A) Africa", "B) Asia", "C) South America", "D) Antarctica"],
            "answer": "A"
        },
        {
            "question": "Who is the author of '1984'?",
            "options": ["A) Aldous Huxley", "B) George Orwell", "C) Ray Bradbury", "D) J.D. Salinger"],
            "answer": "B"
        },
        {
            "question": "What is the primary ingredient in hummus?",
            "options": ["A) Chickpeas", "B) Lentils", "C) Black beans", "D) Green peas"],
            "answer": "A"
        }
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

        user_input = input("You: ").upper()

        if user_input == 'EXIT':
            bot_response = 'You have exited the trivia'
            typing_dots()
            print_slowly(bot_response + '\n')
            bot_response = f"Your final score is: {score}"
            typing_dots()
            print_slowly(bot_response + '\n')
            break
        elif user_input == q["answer"]:
            bot_response = "Correct"
            typing_dots()
            print_slowly(bot_response + '\n')
            score += 1
        else:
            bot_response = f"Incorrect! The correct answer was '{q['answer']}'."
            typing_dots()
            print_slowly(bot_response + '\n')

    # Display final score
    bot_response = f"Your final score is: {score}"
    typing_dots()
    print_slowly(bot_response + '\n')

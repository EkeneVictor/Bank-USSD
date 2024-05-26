import random
import re
import json
import os
import time
from utilities import typing_dots, print_slowly
from ai_games import play_word_association, play_trivia_quiz, play_guess_number
import config


# Load existing responses from a file if it exists
def load_responses(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        return {}


# Save responses to a file
def save_responses(file_name, responses):
    with open(file_name, 'w') as file:
        json.dump(responses, file)


# Define the file to save responses
response_file = 'responses.json'

# Load existing responses
responses = load_responses(response_file)


# Predefined Long responses
class Long:
    R_ADVICE = "Sure, here's some advice..."
    R_EATING = "I like to eat digital bytes!"
    R_PLAY_GAME = "Sure, what game would you like to play!"
    R_GUESS_NUMBER = "Okay then!, I'm thinking of a number between 1 and 100. Try to guess it!"
    R_PLAY_WORD_ASS = "Okay, then!"
    R_PLAY_TRIVIA = "Sure thing!"

    @staticmethod
    def unknown():
        return "I don't know how to respond to that. How should I respond?"


# Add some initial responses
default_responses = {
    "hello": f"Hi there {config.user_name}! How can I help you?",
    "bye": "Goodbye! Have a great day!",
    "help": "Sure, I'm here to help! What do you need assistance with?",
    "name": "I'm a simple chatbot created to assist you with basic questions.",
    "play game": Long.R_PLAY_GAME,
    "guess number": Long.R_GUESS_NUMBER
}

bad_words = ['cunt', 'fuck', 'fucking', 'bitch', 'ass', 'asshole'"damn", "hell", "shit", "fuck", "bitch", "bastard", "asshole",
             "dick", "piss", "cunt", "slut", "whore", "faggot", "nigger", "retard", "motherfucker",
             "crap", "bullshit", "cock", "douche", "dickhead", "prick", "pussy",
             "twat", "wanker", "nigga", "dildo", "bollocks", "bugger", "arse",
             "shithead", "shite", "tits", "knob", "tosser", "sod", "shag", "bloody",
             "git", "minger", "munter", "bellend", "plonker", "wazzock", "arsehole",
             "dickwad", "dipshit", "knobjockey", "cum", "sperm", "spunk", "knobhead",
             "wank", "slag", "skank", "ho", "tramp", "scumbag", "loser", "pisshead",
             "bint", "git", "cocksucker", "turd", "minge", "bitchass", "fuckface",
             "scrote", "knobber", "choad", "pissflaps", "jizz", "jerkoff", "shitfaced",
             "fuckwit", "arsewipe", "craphole", "dickweed", "shitbag", "pissbreath",
             "shitstain", "cumdumpster", "fuckstick", "asshat", "asslicker", "bastardo",
             "ballbag", "pisspants", "cockwomble", "shitbrains", "assclown", "clit",
             "fanny", "gash", "kike", "lesbo", "nutlicker", "pecker", "shitdick",
             "spic", "twunt", "buttfucker", "dicknose", "fucknugget", "nobjockey",
             "punta", "scrotum", "shart", "twatface", "cumguzzler", "fucktard",
             "jizzmopper", "numbnuts", "shitgibbon", "splooge", "twatwaffle", "whorebag",
             "wankstain", "asscock", "bumclat", "fuckhole", "mingebag", "prat",
             "scumbucket", "shitweasel", "tard", "twatwaffle", "wankface", "bumbaclut",
             "cocks", "mothafucka", "schlong", "whore", "dickbag", "shitface", "pussylicker",
             "butthole", "shitshow", "fuckboy", "dickslap", "cockblock", "ballsack",
             "shitty", "cockhead", "numbnut", "pissflap", "cockmongler", "craphead",
             "prickface", "shitbrain", "shitbreath", "pissdick", "douchecanoe", "pissfuck",
             "fuckface", "asspirate", "cuntbag", "bitchtits", "cockmaster", "fuckpuppet",
             "dickweasel", "spermwhale", "asspounder", "assbanger", "fucknut", "shitnugget",
             "cumslut", "cumqueen", "assmuncher", "clitlicker", "cumchugger", "dicktickler",
             "fuckdick", "fuckstick", "motherfuck", "shitstick", "asslicker", "ballsucker",
             "cockbite", "cockburger", "cumbubble", "cumdump", "fudgepacker", "pussyfucker",
             "shitstain", "assranger", "cockfag", "cumbucket", "dickbag", "fuckdouche",
             "fuckhead", "jizzgobbler", "knobgoblin", "pricklicker", "twatface", "wankbucket"
             ]

# Merge default responses with loaded responses, prioritizing loaded ones
responses.update(default_responses)


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Avoid division by zero
    if len(recognised_words) > 0:
        percentage = float(message_certainty) / float(len(recognised_words))
    else:
        percentage = 0

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Add predefined responses
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])
    response(Long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(Long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])
    response(Long.R_PLAY_GAME, ["let's play", "play a game", "play game", "let's a game", ])
    response(Long.R_GUESS_NUMBER,
             ['guess', 'number', 'guessing number', 'guessing', "let's play guessing game", 'guessing game'])
    response(Long.R_PLAY_WORD_ASS,
             ['word', 'association word', 'guessing word association', "let's play word association"])
    response(Long.R_PLAY_TRIVIA, ['play trivia', 'trivia', 'trivia game', 'question trivia'])

    # Check user-defined responses
    for user_input, bot_response in responses.items():
        response(bot_response, user_input.split())

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    if highest_prob_list[best_match] < 1:
        return Long.unknown()
    else:
        return best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Function to learn a new response
def learn_response(user_input, bot_response):
    # Update the responses dictionary
    responses[user_input] = bot_response
    # Save the updated responses
    save_responses(response_file, responses)


def check_for_bad_words(input_text):
    # Split the input into words and remove punctuation
    words = input_text.lower().split()
    words = [word.strip(",.!?;:") for word in words]

    # Iterate over each word and check if it's in the bad words list
    for word in words:
        if word in bad_words:
            return True
    return False


# Main loop to interact with the user
def cipher_ai():
    while True:
        user_input = input('You: ').strip().lower()
        if user_input in ['bye', 'exit', 'see ya']:
            bot_response = get_response(user_input)
            print('\rCipher: ', end='')
            typing_dots()
            print_slowly(bot_response)
            print()
            time.sleep(1.5)
            break
        elif check_for_bad_words(user_input):
            bot_response = random.choice(['brr, get a life....tch', "don't try to teach me corrupt data, I'm not dumb", 'you really should get a life...', 'may the lord be with you.....', ])
            typing_dots()
            print_slowly(bot_response + '\n')
        else:
            bot_response = get_response(user_input)
            typing_dots()
            print_slowly(bot_response + '\n')

            if bot_response == Long.unknown():
                new_response = input('You: ').strip().lower()
                if new_response not in ['forget', 'forget about it', 'dont worry', "don't worry", "don't about it worry", "dont about it worry", 'just forget it']:
                    learn_response(user_input, new_response)
                    bot_response = 'Got it! I\'ll remember that.'
                    typing_dots()
                    print_slowly(bot_response + '\n')
                else:
                    bot_response = 'Okay, I won\'t remember that.'
                    typing_dots()
                    print_slowly(bot_response + '\n')
            elif bot_response == Long.R_GUESS_NUMBER:
                play_guess_number()
            elif bot_response == Long.R_PLAY_WORD_ASS:
                play_word_association()
            elif bot_response == Long.R_PLAY_TRIVIA:
                play_trivia_quiz()

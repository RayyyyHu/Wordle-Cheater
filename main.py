import random
from random import shuffle

alternatives = []
allLetters = []
guess = ['', '', '', '', '']

class Letter:

    """
    - color: represent the color assigned to this letter. Empty if the letter is not used
    - invalid Position: the position where the letter appears yellow.
    (Note: for color, we ONLY care about whether its grey or not. If the color of is green or yellow, its information will be stored in the position array. Also, when a letter is grey, it will not change to green or yellow in any cases)
    """

    def __init__(self):
        self.color = ""
        self.invalidPosition = []


def init():

    global allLetters
    global alternatives
    global guess

    WORDS = open("static/Scrabble Dictionary.txt")
    allLetters = []

    # Find all words with a length of 5

    for word in WORDS:

        word = word.upper().strip()

        if len(word) == 5:
            alternatives.append(word)

    # Initialize the status of each letter

    for i in range(26):
        allLetters.append(Letter())
    
    # Initialize the possible words (If a letter appears green, we store it into this list)
    
    guess = ['', '', '', '', '']
        

def read_usr_input():

    global alternatives

    print("1. 'continue':    input your result for a new word")
    print("2. 'print':       print all valid words")
    print("3. 'check':       check if a word is valid")
    print("4. 'recommend':   recommend words to input")
    print("5. 'reset':       reset the round")
    print("Please enter a number: ", end = '')
    t = input()
    print()

    if t == "1":

        print("On the first line, enter the five letters you've guessed, separated by a space.")
        print("On the second line, enter corresponding five colors for the five letters, respectively, separated by a space.")
        print("For the colors: enter 'grey' for grey, 'yellow' for yellow, and 'green' for green")

        l = input().upper().split(' ') # the five letters
        c = input().lower().split(' ') # their corresponding color

        process(l, c)
    
    if t == "2":
        
        print_all()
    
    if t == "3":

        check_word()

    if t == "4":

        recommend()
    
    if t == "5":

        init()

        print("#--------------------------------------------------------------------------------------------------------------------------#")

def process(currentLetters, currentColors):

    global allLetters
    global guess

    for i in range(5):

        currentLetter = currentLetters[i]
        currentColor = currentColors[i]
        currentIndex = ord(currentLetter) - ord('A')

        if currentColor == "grey" and allLetters[currentIndex].color == "": # The letter appear as grey for the FIRST time
            
            allLetters[currentIndex].color = "grey"
        
        if currentColor == "yellow": # The letter should not appear at the current position but is in the word
            
            allLetters[currentIndex].color = "yellow"
            allLetters[currentIndex].invalidPosition.append(i)
        
        if currentColor == "green": # The letter should appear at the current position
            
            allLetters[currentIndex].color = "green"
            allLetters[currentIndex].pos = i
            guess[i] = currentLetter
    
    eliminate()


def eliminate():

    global alternatives
    global allLetters
    global validLetters

    t = []

    for alternative in alternatives:
        
        valid = True

        for i in range(len(alternative)):

            currentIndex = ord(alternative[i]) - ord('A')

            # Case 1: the letter is grey, which means the letters does appear in the target word
            
            if allLetters[currentIndex].color == "grey":
                valid = False
            
            # Case 2: the letter is yellow, which means the letter should not occur at the current position

            if i in allLetters[currentIndex].invalidPosition:
                valid = False

            # Case 3: the letters is green, which means the letter should occur at the current position

            if guess[i] != '' and alternative[i] != guess[i]:
                valid = False

            # Case 4: the letter is non-grey, but does not appear in the word

            for i in range(26):

                currentLetter = chr(ord('A') + i)

                if (allLetters[i].color == "yellow" or allLetters[i].color == "green") and currentLetter not in alternative:
                    valid = False

        # Add the valid word into the alternatives

        if valid:
            t.append(alternative)
    
    alternatives = t[:]


def print_all():

    global alternatives

    for alternative in alternatives:
            print(alternative)


def check_word():

    global alternatives

    print("Please input the word you want to check in upper case: ", end = '')
    t = input().upper()
    print()

    print("The word is valid.") if t in alternatives else print("The word is not valid.")


def recommend():

    global alternatives

    # Note: after the elimination process, all words that are invalid are kicked out of the alternatives list
    # the remaining words have:
    # 1. the green letter occurring at the current position
    # 2. the yellow letter included in the word at a valid position
    # (i.e., if the letter appears yellow at the second position, then all words with the letter at the second position is kicked out of the elimination lists)
    # 3. the grey letter not occurring in the word
    #
    # That is to say, all the remaining words have EQUAL probability of being correct.
    # Therefore, I simply randomly choose ten words in the alternatives

    t = alternatives[:]

    for i in range(10):

        random.shuffle(t)

        print(t[0])

        if len(t) > 1:

            t = t[1:]
        
        else:

            break


#----------------------------------------------------------------------------------------------------------------------------------------------#

init()

while True:

    read_usr_input()
    print()
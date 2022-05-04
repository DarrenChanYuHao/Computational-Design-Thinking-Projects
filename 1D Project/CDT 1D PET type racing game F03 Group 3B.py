#====================================================================================================
# Import Libraries
#====================================================================================================
from libdw import pyrebase #For the  multiplayer aspect
import os # For clearing screen if needed
import time # For timer based actions
import msvcrt # For non-paused user inputs
#====================================================================================================

#====================================================================================================
# Firebase auth setups
#====================================================================================================
projectid = "myctdproject-chan-darren-default-rtdb"
dburl =  "https://ctd-1d-pet-racing-game-default-rtdb.asia-southeast1.firebasedatabase.app/"
authdomain = "https://ctd-1d-pet-racing-game-default-rtdb.asia-southeast1.firebasedatabase.app/"
apikey = "AIzaSyBZE2wh1Hwo0I3OP3y-qzE2uqLktQNfOPA"
email = "ctd1dpetracing@gmail.com"
password = "ctd1dpetracing"

config = {
    "apiKey": apikey,
    "authDomain": authdomain,
    "databaseURL": dburl,
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()
user = auth.refresh(user['refreshToken']) 
#====================================================================================================

#====================================================================================================
# Functions
#====================================================================================================

# This function is to get the english word list that is in the firebase database
def get_dictionary():
    
    key = "Dictionary" #Calling the english word list node

    node = db.child(key).get(user['idToken']) 
    english_dictionary = node.val() 
    return english_dictionary.split(' ')

# Get player input and check if it is in the word list
# Prefix is the current prefix that is inputted by player 1 while the english dictionary is the string of words to check against
# The function will ask the player to key in a word and return if the word is in word list or not, if it is, it will return True, else it will return False
def player_input_word(prefix,english_dictionary,wordlogger): 

    print("Key in your word")
    player_word = (prefix + input("{}".format(prefix)) ).lower()
    if player_word in english_dictionary and player_word not in wordlogger:
        set_wordlogger(wordlogger,player_word) # adds player_word into wordlogger 
        return True
    else: 
        return False

# Get player 1 to input a prefix string to be used in this round
# After player set the prefix string, it will be set in the prefix string node in the firebase database, it will also return the prefix string
def player_input_prefix():

    prefix = input("Key in this round's prefix: ")
    prefix = prefix.upper()

    key = "prefix"
    db.child(key).set(prefix, user['idToken'])

    return prefix

# This function get the current round's prefix from the prefix node in the firebase database
def get_prefix():
    key = "prefix"

    node = db.child(key).get(user['idToken']) 
    prefix = node.val()
    return prefix

# This function allows the player to choose their player number
# It increase the player count node in the database by 1, once the player have successfully chosen his player number
def choose_player(): #player_number_initialization
    
    done = False

    player_count = 0

    print("{} player(s) waiting in the lobby.\nPress 'y' to join, 'n' to quit!(Press 'r' to reset if game is stuck)".format(player_count)) # For initial player_count

    while not done:

        previous_player_count = player_count
        key = "player_count"
        node = db.child(key).get(user['idToken'])
        player_count = node.val()

        if(previous_player_count != player_count): # The line will only print once when there has been a change in number of player in lobby
            os.system('cls')
            print("{} player(s) waiting in the lobby.\nPress 'y' to join, 'n' to quit! (Press 'r' to reset if game is stuck)".format(player_count)) # New players have to press 'y' to join the game

        if msvcrt.kbhit():

            player_input = msvcrt.getch().decode('ASCII').lower()

            if player_input == 'y':
                done = True
                player_count += 1
                db.child(key).set(player_count, user['idToken'])
                print("Welcome Player {}!".format(player_count))
                return player_count

            if player_input == 'n': # New players press 'n' will exit
                print("You have quit")
                time.sleep(2)
                raise TypeError

            if player_input == 'r':
                reset_stage(0)

# This function checks whose turn it current is by getting the current_player node from the database
def get_current_player():
    
    key = "current_player"

    node = db.child(key).get(user['idToken']) 
    current_player = node.val()
    return current_player

# This function set whose turn it current is by updating the current_player node from the database
def set_current_player(current_player):
    key = "current_player"
    db.child(key).set(current_player, user['idToken'])

# This function counts how many players are currently in the game via the player_count node from the database
def get_player_count():
    key = "player_count"

    node = db.child(key).get(user['idToken']) 
    player_count = node.val()
    return player_count

# This function set the max number of players allowed in this round by updating the set_max_number_of_players node from the database
def set_max_number_of_players():

    number_of_players = int(input("Set number of players in this round: "))
    
    key = "max_number_of_players"
    
    #======================================================================================================================
    players_alive = []
    
    for player_name in range(1,number_of_players+1):

        add_to_dictionary = {str(player_name):20} #Initialise each player with 20 HP
        
        db.child('Health').update(add_to_dictionary, user['idToken'])

        players_alive.append(str(player_name))
    
    db.child('players_alive').set(players_alive,user['idToken'])
    #======================================================================================================================

    db.child(key).set(number_of_players, user['idToken'])
    

# This function get the max number of players allowed in this round by checking the set_max_number_of_players node from the database
def get_max_number_of_players():
    key = "max_number_of_players"

    node = db.child(key).get(user['idToken']) 
    number_of_players = node.val()
    return number_of_players      

# This function set the board set up readiness of this round by taking in a string that check if it is "Start Game", if it is, it will set the game status to True
# which means the game is ready to start
def set_check_set_up_status(key):

    if(key == "Start Game"):
        key = "set_up_status"
        db.child(key).set(True, user['idToken'])

# This function check if the game is ready to start by checking the set_up_status node from the database, if it is, it will return True, else it will return False
def get_check_set_up_status():
    key = "set_up_status"

    node = db.child(key).get(user['idToken']) 
    set_up_status = node.val()
    return set_up_status

def get_players_alive():

    key = "players_alive"
    
    node = db.child(key).get(user['idToken']) 
    
    get_players_alive = node.val()
    
    return get_players_alive

def set_players_alive(players_alive):
    db.child('players_alive').set(players_alive,user['idToken']) 

def get_wordlogger():
    key = "wordlogger"
    node = db.child(key).get(user['idToken']) 
    return node.val()

def set_wordlogger(wordlogger,word):
    wordlogger.append(word)
    db.child('wordlogger').set(wordlogger,user['idToken']) 

def get_health():
    key = "Health"
    node = db.child(key).get(user['idToken']) 
    return node.val()

def set_health(health):    
    db.child('Health').set(health,user['idToken'])

# This function resets the board by resetting all the node values to pre-game start values
# Specifically :
# 1. Player count is reset back to 0
# 2. Current player is reset back to player 1
# 3. Set up readiness is reset to false
# 4. Max number of players is reset back to min 2
# 5. Prefix is reset to blank
# 6. Reset wordlogger

def reset_stage(player_number):
    
    key = "player_count"
    
    if(player_number == 1):
        db.child(key).set(1, user['idToken'])
    else:
        db.child(key).set(0, user['idToken'])

    key = "current_player"
    db.child(key).set('1', user['idToken'])

    key = "set_up_status"
    db.child(key).set(False, user['idToken'])
    
    key = "max_number_of_players"
    db.child(key).set(999, user['idToken']) #Set initial max_number_of_playeers to 999

    key = "prefix"
    db.child(key).set(" ", user['idToken'])

    db.child('wordlogger').set([''], user['idToken'])
#====================================================================================================

#====================================================================================================
# Startup and Global Variables
#====================================================================================================

# Get a string of english words using the get_dictionary method and setting it to the string variable english_dictionary
english_dictionary = get_dictionary()

# Count how many players are currently registered in the game and setting it to the int variable player_count
player_count = get_player_count()

#Check what is the max number of player allowed for this round and setting it to the int variable max_player_count
max_player_count = get_max_number_of_players()

# This if else here is to check if the lobby is full by comparing if the current player count exceeds the max number of players allowed
# Why we if else here first and then do a while loop inside is because we want to only print the line telling player that it is full once while secretly looping
# to check status whether it is still full!
# *Note: Currently, have yet to code the game to allow player in once game have slots
if(player_count >= max_player_count):

    print("Sorry the lobby is full for this round!")

    while(player_count >= max_player_count): #In while loop, we use less than or equal to, cause you have not indicated your player choice, so you are not counted in player_count
        check_admin = input("reset the lobby by typing admin: ").lower() # This is a force reset because otherwise if ppl dont have access to database cannot reset

        if(check_admin == "admin"):

            reset_stage(0)
            player_count = get_player_count() #These needs to be here to update the player_count and max_player_count values if not it will be stuck in an infinite loop
            max_player_count = get_max_number_of_players()
            
player_number = choose_player() #Allow player to join the game by selecting their player number

set_up_status = get_check_set_up_status() #Check if game is ready to be played!

# If you are player 1, special actions are required as you will be considered the host
# Spcifically :
# 1. Resetting the game to start conditions
# 2. Entering the prefix to be used in this round
# 3. Setting the max number of players (If the game already have 3 registered player and you choose 2 max player instead
# the 3rd player will become a spectator)
# 4. Informing the program that the game is set up and ready to be played

if (player_number == 1):
    
    # Reset Stage
    reset_stage(player_number)

    # Start new stage
    prefix = player_input_prefix()
    number_of_players = set_max_number_of_players()
    set_up_status = set_check_set_up_status("Start Game")

else: #This is for if you are not player 1

    # You will check the number of registered players and max allowed players again as the player 1 might have changed it/people might have joined while you were idling
    # in the "choosing_player" function input screen
    player_count = get_player_count()
    max_player_count = get_max_number_of_players()

    # If it turns out you joined too late, it will tell you the lobby is full
    if(player_count > max_player_count): #This one is less than only
        print("Sorry the lobby is full for this round!")
        time.sleep(5)
        raise TypeError

    # This part waits for the game to be done setting up by player 1
    if(set_up_status != True):
        print("Waiting for Player 1 to finish setting up!")
        while(set_up_status != True):
            set_up_status = get_check_set_up_status()
    
    #Once game is set up, you will get the prefix set up by player 1 for this round
    prefix = get_prefix()

# This will set the current turn universally across all registered player to the same player
current_player_turn = get_current_player()
#====================================================================================================

#====================================================================================================
# Main Game
#====================================================================================================

max_player_count = get_max_number_of_players()

while True:

    players_alive = get_players_alive()                 # Check who is alive and store it into list players_alive

    if(player_count < max_player_count):

        print("Waiting for other players to join!")

        while(player_count < max_player_count):     # If the lobby isn't filled, wait for everyone to join
            player_count = get_player_count()
        
        print("The game has started") # This will only print when the player exits the above while loop and show to player the game have started

    if (player_number != current_player_turn):      # If it isn't your turn then you wait

        print("It is now player {} turn".format(current_player_turn))

        while (player_number != int(current_player_turn)): # If it's not your turn, spam query

            previous_player_turn = current_player_turn      # This will be used to check if there has been any change in player
            current_player_turn = get_current_player()      # Keep querying current player's turn
            players_alive = get_players_alive()             # Check who is alive
            wordlogger = get_wordlogger()
            
            if(current_player_turn != previous_player_turn):

                if(str(current_player_turn) in players_alive):
                    print("It is now player {} turn".format(current_player_turn))
                    print("These are the current words that have been entered: {}".format(wordlogger[1:]))

            if len(players_alive) == 1:     # When overall game concludes (aka not just when you lose), this is the what will be shown to all the losers
                if (str(player_number) not in players_alive):

                    set_current_player(int(players_alive[0]))  
                    input('The game is over, try harder next time!')
                    raise TypeError

    while(player_number == int(current_player_turn)):  # If it is your turn, player_number is stored as an integer

        if (str(player_number) not in players_alive):   # If you have lost, code will go to the next turn

            next_player_number = player_number +1

            if next_player_number > max_player_count:
            # Points to the first player to continue finding the next player if we reached the end of the player_list

                next_player_number = 1

            set_current_player(next_player_number)      
            current_player_turn = get_current_player()

            continue

        players_alive = get_players_alive() # Somebody might have died when you were waiting for other players turn to finish, so we check player_alive again

        if(len(players_alive) == 1 ): # If theres only 1 player surviving

            if (player_number == int(players_alive[0])): # Check if the player_number is the last survivor

                reset_stage(0) # Reset game after game over
                input('You are the champion!')
                raise TypeError     # Exit code

        health = get_health()                           # We will refer to everyone's health in a dictionary e.g. {'1':20, '2':20, '3':20}
        wordlogger = get_wordlogger()                   # wordlogger will check if the word has been used by the players e.g. ['also','astronaut']
        correct = False
        start = time.time()                             # Start a timer to calculate to later calculate the time taken for this turn by the current player

        while(correct == False):                        # Only break while loop if user has entered an appropriate respones i.e. a word that hasn't been keyed in
            
            correct = player_input_word(prefix,english_dictionary,wordlogger)
            if(correct == False):
                print("Not a valid word")

            time_used = time.time() - start             # Calculates the time that has elapsed since the player entered and answer
                                                        # This will be used to deduct the player's health

            if time_used > health[str(player_number)]:   # If player's health is less than the time he used, it will disqualify him, causing him to lose
                break
    
        health[str(player_number)] = round(float(health[str(player_number)]) - time_used,2) # round off to 2d.p and store into the database

        print("This is remaining hp: {}".format(health[str(player_number)]))

        if health[str(player_number)] > 0:   # Only store data if the health isn't negative
            set_health(health)

        else:                               # Player has lost the game

            del health[str(player_number)]      # Delete the health of the player i.e. deletes the dictionary key

            players_alive.remove(str(player_number))    # Remove losers from players_alive list e.g. ['2','4']
            set_health(health)                  
            set_players_alive(players_alive)
            print('You have lost, better luck next time')

        next_player_number = player_number + 1       # Change turn

        if next_player_number > max_player_count: # If the next player is player 1
            next_player_number = 1                  

        set_current_player(next_player_number)  # Next player's turn
        current_player_turn = get_current_player()
        
#==================================================================================================== Thank you for readng our code :)
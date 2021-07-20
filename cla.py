import requests 
import pandas as pd
import json
from chess import pgn

opening_db = {}
data = None
# ------------ Settings ---------------
with open('settings.json') as f:
    settings = json.load(f)

ratings, speeds = [], []
for r in settings['Average Ratings']:
    if settings['Average Ratings'][r]: 
        ratings.append(r)

for t in settings['Time Controls']:
    if settings['Time Controls'][t]:
        speeds.append(t)

# ------------ FUNCTIONS ----------------
def cla_definitions():
    print(""" DEFINITIONS:
    Name - This a user defined title to a particular game. This can help identify a unique PGN. Use option "6" to edit this name. 
    Moves - The total amount of moves made in the game
    Total Games - The number of games that have reached the same board position
    Game Prob. - The probability of a particular player playing each move recorded in the game's PGN according to the Lichess opening explorer.
    Avg Prob. - The average probability of each move being played in the game 
    PGN - Portable Game Notation (PGN) is a common digital notation for chess games
    (W) - Refers to the player playing with the White pieces
    (B) - Refers to the player playing with the Black pieces
    """)


def cla_edit():
    try: 
        row = int(input("Enter the row's index number that you would like to set a name to: "))
        if row < 0 or row > data.shape[0]:
            print("Invalid row number")
        else:
            name = input("Enter a name: ")
            return row, name
    except ValueError:
        print("Invalid row number")
    return -1, None
    

def cla_calculate(game):
    game_prob = [1,1]
    move_prob = [[],[]]
    count = 0
    board = game.board()
    for i,move in enumerate(game.mainline_moves()):
        count += 1
        fen = board.fen()
        info = opening_db[fen] if fen in opening_db else lichess_query(fen)
        total_games, move_total = 0, 0
        for candidate_move in info['moves']:
            total_games += candidate_move['white']+candidate_move['draws']+candidate_move['black']
            if candidate_move['uci'] == move.uci():
                move_total = candidate_move['white']+candidate_move['draws']+candidate_move['black']
        game_inc = 0.1/(total_games+1) if move_total == 0 else move_total*1.0/total_games    
        
        game_prob[i % 2] *= game_inc
        move_prob[i % 2].append(game_inc)       

        board.push(move)

    return game_prob, [sum(move_prob[0])/len(move_prob[0]),sum(move_prob[1])/len(move_prob[1])], board.fen(), count


def lichess_query(fen):
    query = {
      'variant':'standard',
      'fen':fen,
      'recentGames':0,
      'topGames':0,
      'speeds[]':speeds,
      'ratings[]':ratings
    }
    response = requests.get("https://explorer.lichess.ovh/lichess", params=query)
    opening_db[fen] = response.json()
    return response.json()


def cla_create():
    games = []
    name = ""
    # Fetch FENs
    if cla_load(games,name):
        # Create Table 
        cla_build(games, name)


def cla_build(games, name, new=True):
    d = {
      'Name' : [],
      'Moves' : [],
      'Total Games' : [],
      'Game Prob. (W)' : [],
      'Avg Prob. (W)' : [],
      'Game Prob. (B)' : [],
      'Avg Prob. (B)' : [],
      'PGN' : []
    }

    for num,game in enumerate(games):
        if num % 50 == 0 and num != 0:
            print("Calculating Game {}...".format(num))
        game_score, move_score, fen, moves = cla_calculate(game)
        info = opening_db[fen] if fen in opening_db else lichess_query(fen)
        d['Name'].append(name)
        d['Moves'].append(moves)
        
        d['Game Prob. (W)'].append(game_score[0])
        d['Avg Prob. (W)'].append(move_score[0])
        d['Game Prob. (B)'].append(game_score[1])
        d['Avg Prob. (B)'].append(move_score[1])

        d['Total Games'].append(info['white']+info['draws']+info['black'])
        d['PGN'].append(game.variations[0])

    global data
    if new: # Make new dataframe
        data = pd.DataFrame(data=d)
        cla_show()
    else:
        data_temp = pd.DataFrame(data=d)
        data = data.append(data_temp, ignore_index=True)
    

def cla_show():
    print(data)
    # Table Manipulation
    while True:
        print("""\nPlease select one of the following options by entering the corresponding number
    1. Sort Table by Number of Moves
    2. Sort Table by Total Games
    3. Sort Table by Game Probability (W/B)
    4. Sort Table by Average Game Probability (W/B)
    5. Sort Table by Game Index
    6. Edit Name of row
    7. Add a PGN file to the table
    8. Header Definitions
    9. Return to main menu""")
        ans = input()
        if ans == "1" or ans == "2":
            col = { "1" : "Moves", "2" : "Total Games"}
            print(data.sort_values(by=[col[ans]], ascending=False))
        elif ans == "3":
            color = input("White (W) or Black (B): ").lower()
            if color in ["white","w","black","b"]:
                if "w" in color:
                    print(data.sort_values(by=['Game Prob. (W)'], ascending=False))
                else:
                    print(data.sort_values(by=['Game Prob. (B)'], ascending=False))
        elif ans == "4":
            color = input("White (W) or Black (B): ").lower()
            if color in ["white","w","black","b"]:
                if "w" in color:
                    print(data.sort_values(by=['Avg Prob. (W)'], ascending=False))
                else:
                    print(data.sort_values(by=['Avg Prob. (B)'], ascending=False))
        elif ans == "5":
            print(data)
        elif ans == "6":
            pos,name = cla_edit()
            if pos != -1:
                data.loc[pos,'Name'] = name
            print(data)
        elif ans == "7":
            games = []
            name = ""
            # Fetch FENs
            if cla_load(games, name):
                # Create Table 
                cla_build(games,name,new=False)
                print(data)
        elif ans == "8":
            cla_definitions()
        elif ans == "9":
            break


def cla_load(games,fn):
    fn = input("Enter a valid file in PGN format to load: ")
    try:
        with open(fn) as f:
            max_moves = int(input("Set a max number of moves to analyze: "))
            game = pgn.read_game(f)
            while game:
                game.board() # Check if valid, otherwise throws attribute error
                games.append(game)
                game = pgn.read_game(f)
            return True
    except FileNotFoundError:
        print('The file "{}" was not found.'.format(fn))
    except AttributeError:
        print('Error reading "{}". Please submit a valid file that uses PGN format.'.format(fn))
    except ValueError:
        print('Invalid max_move parameter')
    return False

def cla_import():
    try:
        fn = input("Enter a the name/path of a CSV file to import: ")
        global data
        data_temp = pd.read_csv(fn)
        structure = ['Name', 'Moves', 'Total Games', 
                    'Game Prob. (W)', 'Avg Prob. (W)', 
                    'Game Prob. (B)', 'Avg Prob. (B)', 
                    'PGN']
        for i,col in enumerate(data_temp.columns):
            if structure[i] != col:
                print("Error Reading CSV, please make sure it conforms to the structure of a CLA table")
                return
        data = data_temp
        print('File "{}" has been successfully imported!'.format(fn))
        cla_show()
    except FileNotFoundError:
        print('File "{}" is not found'.format(fn))

def cla_export():
    if data is not None:
        fn = 'cla_results.csv'
        data.to_csv(fn, index=False, header=True)   
        print('The CLA table has been successfully exported to {}'.format(fn))         
    else:
        print("There is no current CLA Table, try either creating or importing one to get started.")
        

# ----------------- MAIN ------------------
options = {
    "1" : cla_create,
    "2" : cla_import,
    "3" : cla_export,
    "4" : exit,
}
print("""-------------------------------------------------
Welcome To the Chess Line Analysis (CLA) Program
-------------------------------------------------""")
while True:
    print("""\nPlease select one of the following options by entering the corresponding number
    1. Create a new CLA table.
    2. Import a CLA table
    3. Export a CLA table
    4. Exit""")
    ans = input()
    if ans in options:
        options[ans]()

response = requests.get("https://explorer.lichess.ovh/lichess", params=query)
print(response)
print(response.json())
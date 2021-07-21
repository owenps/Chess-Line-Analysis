# Chess Line Analysis Program
![Python Badge](https://img.shields.io/badge/Python-007396?style=for-the-badge&labelColor=black&logo=Python&logoColor=white) 
![Lichess Badge](https://img.shields.io/badge/Lichess-FF6767?style=for-the-badge&labelColor=black&logo=Lichess&logoColor=white) 

The Chess Line Analysis (CLA) Program is a chess tool to compare and analyze PGNs to help you make better use of your study time. The goal here is to outline particular games/lines which are statistically the most likely to happen. The CLA program is built using Python and queries the [Lichess Opening-Explorer database](https://lichess.org/api#tag/Opening-Explorer) for its statistics. 

Please refer to the following sections to get a better idea of what the script does and how it works. If you are looking for something more visual, I would recommend checking out [chesstree.net](http://www.chesstree.net/). 

A big thank you to [u/Rumer57](https://www.reddit.com/user/rumer57) for the idea and the continuous support and feedback throughout the project's development.

If you enjoy the project and wish to show your support, leaving a ⭐ on the repository would really mean a lot!

## What Does It Do?

- Imports a PGN and calculates the probability of the PGN occuring (according to the Lichess Opening Explorer).
- Creates a CLA table storing and displaying all the games analyzed and gives you options to view the data.
- Export a CLA table to a .CSV file
- Import a .CSV CLA table to expand/edit the table. 
- Assign names to PGNs for easier reference (E.g. "Stafford Gambit h3")
- Configure the script to analyze particular time controls or set of ratings. Visit the `settings.json` file to customize your experience. 

## What Does It *Not* Do?

- Analyze different branches in a PGN. Currently the script only considers the mainline moves. Please consider breaking the PGN into multiple PGNs for each branch you wish to process. 
- Evaluate the positions with an engine. Please use the [Stockfish](https://stockfishchess.org/) or any publicly available chess engine.  
- Give you recommendations on what to play. The program should guide you how to structure your study time. Do your own research (accompanied with an engine) to make sure you are comfortable playing a particular line. 

## Executing the Script Yourself
To execute `cla.py` you will first need the following dependecies. We will use `pip` for our installer. One option is the install them individually by executing the three commands:

```
pip install chess
pip install pandas
pip install requests
```
Or to install them all at once, use the following command. 
```
pip install -r requirements.txt
```
To then run the script, execute
```
python cla.py
```

## FAQ

> How do I only look at rapid/classical games? <br> How do I only view games within my rating?

Inside the `settings.json` file you can configure all the database settings which include time controls and ratings. Simply open the file in notepad or your favourite text editor and change whichever `true` values to `false` or vice versa. 

> Does this include the Lichess masters database? 

No 

> What is `Avg Prob.` ? 

`Avg Prob.` is short for average move probability. Each move in the game has an associate probability attached to it. This is simply the chance of a player (White or Black) playing that move. So `Avg Prob.` is the sum of these probabilities divided by the total number of moves a particular player has made. It is a metric to answer the question: "On average, how popular are the moves a player made?". 

> What is `Game Prob.` ?

`Game Prob.` is similar to `Avg Prob.` except we take the product of each of the move probabilities. This produces the probability of that game actually occuring. 

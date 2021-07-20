# Chess Line Analysis Program
![Python Badge](https://img.shields.io/badge/Python-007396?style=for-the-badge&labelColor=black&logo=Python&logoColor=white) 
![Lichess Badge](https://img.shields.io/badge/Lichess-FF6767?style=for-the-badge&labelColor=black&logo=Lichess&logoColor=white) 

The Chess Line Analysis (CLA) Program is a chess tool to compare and analyze PGNs to help you make better use of your study time. The goal here is to outline particular PGNs which are the most likely to happen. The CLA program is built using Python and querys the [Lichess Opening-Explorer database](https://lichess.org/api#tag/Opening-Explorer) for its statistics. A big thank you to [u/Kael57](https://www.reddit.com/user/Kael57) for the idea for this project and the feedback throughout its development. 

If you enjoy the project and wish to show your support, leaving a ⭐ on the repository would really mean a lot!

## What Does It Do?

- Imports a PGN and calculates the probability of the PGN occuring (according to the Lichess Opening Explorer).
- Creates a CLA table storing and displaying all the games analyzed and gives you options to view the data.
- Export a CLA table to a .CSV file
- Import a .CSV CLA table to expand/edit the table. 
- Assign names to PGNs for easier reference (E.g. "Stafford Gambit h3")
- Configure the script to analyze particular time controls or set of ratings. Visit the `settings.json` file to customize your experience. 

## What Does It Not Do?

- Analyze different branches in a PGN as it only considers the mainline moves. Please consider breaking the PGN into multiple PGNs for each branch you wish to process. 
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
Then to run the script execute
```
python cla.py
```

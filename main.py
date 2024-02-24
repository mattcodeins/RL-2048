from datetime import date
from game import Game

game = Game()
if game.run():
    s = input('Enter your name: ')
    s += ' ' + str(game.score) + ' ' + date.today().strftime("%d/%m/%Y") + '\n'
    with open('highscores.txt','a') as f:
        f.write(s)
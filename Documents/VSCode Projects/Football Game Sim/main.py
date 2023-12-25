import tkinter as tk
from tkinter import ttk
from game import *

class FootballSimGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Football Simulation GUI")
        self.game = game

        # Create GUI elements
        self.score_label = ttk.Label(self, text="Score: 0 - 0")
        self.score_label.pack(pady=10)

        self.stats_label = ttk.Label(self, text="Stats: ")
        self.stats_label.pack(pady=10)

        self.play_button = ttk.Button(self, text="Simulate Play", command=self.simulate_play)
        self.play_button.pack(pady=10)

        self.quarter_button = ttk.Button(self, text="Simulate Quarter", command=self.simulate_quarter)
        self.quarter_button.pack(pady=10)

        self.end_game_button = ttk.Button(self, text="End of Game", command=self.end_of_game)
        self.end_game_button.pack(pady=10)

    def update_gui(self):
        # Update score label
        score_text = f"Score: {self.game.home_score} - {self.game.away_score}"
        self.score_label.config(text=score_text)

        # Update stats label (add relevant stats)
        stats_text = "Stats: ..."
        self.stats_label.config(text=stats_text)

    def simulate_play(self):
        # Implement logic to simulate one play
        # This should call the necessary functions from your game logic
        # Update game state
        self.game.simulate_one_play()

        # Update GUI
        self.update_gui()

    def simulate_quarter(self):
        # Implement logic to simulate one quarter
        # This should call the necessary functions from your game logic
        # Update game state
        self.game.simulate_one_quarter()

        # Update GUI
        self.update_gui()

    def end_of_game(self):
        # Implement logic to simulate the end of the game
        # This should call the necessary functions from your game logic
        # Update game state
        self.game.simulate_end_of_game()

        # Update GUI
        self.update_gui()

if __name__ == "__main__":
    # Create an instance of the FootballGame class
    game = Game(teams[0],teams[1])

    # Create and run the GUI
    app = FootballSimGUI(game)
    app.mainloop()
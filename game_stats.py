class GameStats:
    """Track Stats of the game."""
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0
        text_file = "all_time_high_score.txt"
        with open('all_time_high_score.txt') as f:
            high_score = f.read()
        self.all_time_hs = int(high_score)
        # Level
        self.level = 1

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ship_left = self.settings.ship_limit
        self.score = 0
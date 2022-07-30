import pygame.font
from pygame.sprite import Group

from ship_nosa import Ship

class Scoreboard:
    """A class of scoring info."""
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.prep_ships()

    # Font settings for scoring info
        self.text_color = (30, 30, 30)
        self.high_score_text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

    # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_all_time_score()

    def prep_ships(self):
        """Show how many ship are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 5 + ship_number * ship.rect.width
            ship.rect.y = 5
            self.ships.add(ship)

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

    # Display the score at the top right of the corner.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn high score into a redered image."""
        high_score = round(self.stats.high_score, -1)
        high_Score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_Score_str, True, self.high_score_text_color, self.settings.bg_color)

        # center the score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_all_time_score(self):
        all_time_hs = round(self.stats.all_time_hs, -1)
        all_time_hs_str = "{:,}".format(all_time_hs)
        self.all_time_hs_image = self.font.render(all_time_hs_str, True, self.high_score_text_color, self.settings.bg_color)
        self.all_time_hs_rect = self.all_time_hs_image.get_rect()
        self.all_time_hs_rect.centerx = self.screen_rect.centerx - 200
        self.all_time_hs_rect.top = self.score_rect.top

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.all_time_hs_image, self.all_time_hs_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def check_all_time_hs(self):
        if self.stats.high_score > self.stats.all_time_hs:
            self.stats.all_time_hs = self.stats.high_score
            with open('all_time_high_score.txt', 'w')  as f:
                f.write(str(self.stats.high_score))
            self.prep_all_time_score()

    def prep_level(self):
        """Turn level into rendered image."""
        level_str = 'lv ' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
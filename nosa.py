import sys, pygame
from time import sleep

from settings import Settings

from ship_nosa import Ship

from bullet import Bullet

from alien import Alien

from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

class AlienInvasion:
	"""Overall class to manage game assets and behvior."""
	def __init__(self):
		"""Initialize the game, create game resources."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		# Set game caption
		pygame.display.set_caption("Alien Invasion")

		# Create instance to store game stats.
		self.stats = GameStats(self)

		# Instance of ship, bullets, aliens
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()

		# Instance of play button
		self.play_button = Button(self, 'Play')

		# Instance of score board
		self.sb = Scoreboard(self)


	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_alien()

			self._update_screen()

		# Redraw the screen during each pass through the loop.
			

	def _check_events(self):
		"""Respond to keypress and mouse events."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_event(event)


	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Play."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self.settings.initialize_dynamic_settings()
			# reset game stats.
			self.stats.reset_stats()
			self.stats.game_active = True

			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			# Get rid of any remanining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()
			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()

			# Hide the mouse cursor.
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_UP:
			self.ship.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_event(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
		elif event.key == pygame.K_UP:
			self.ship.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = False

	def _update_bullets(self):
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		print(len(self.bullets))
		self._check_bullet_alien_collisions()
		# Check if bullet hit alien.
			# If hit get rid of both.
		
	def _check_bullet_alien_collisions(self):
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
				self.sb.prep_score()
				self.sb.check_high_score()
				self.sb.check_all_time_hs()
		if not self.aliens:
			# Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

		# Increase level.
			self.stats.level += 1

	def _ship_hit(self):
		"""Respond to the ship being hit by an alien."""
		if self.stats.ship_left > 0:

			# Decrement ship left and update score
			self.stats.ship_left -= 1
			self.sb.prep_ships()
			# Get rid of any remanining aliens and bullets.
			self.aliens.empty()  
			self.bullets.empty()
			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()
			# Pause
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)


	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _create_fleet(self):
		"""Create a fleet of alien."""
	# Make an alien and find number of alien can fit in a row.
	# Space between them is equal to its width.
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

	# Determine the number of rows of aliens that fit on the screen.
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 
			(3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

	# Create full fleet of aliens.
		for row_number in range(number_rows):


		# Create the first row of aliens.
			for alien_number in range(number_aliens_x):
		 	# Create an alien and place it in the row.
		 		self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in the row."""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width  * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _update_alien(self):
		"""Update the positions of all aliens in the fleet."""
		self._check_fleet_edges()
		self.aliens.update()
		self._check_aliens_bottom()
		# Check ship and alien collisions.
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction."""
		for alien in self.aliens.sprites():
			alien.rect.y += 2 * self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _check_aliens_bottom(self):
		"""Check if any alien have reached the bottoms."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Treat this same as if the ship got hit.
				self._ship_hit()
				break

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		# Draw the score board.
		self.sb.show_score()

		#Draw the play button if the game is inactive.
		if not self.stats.game_active:
			self.play_button.draw_button()

		# Make the most recently drawn screen visible.
		pygame.display.flip()

if __name__ =='__main__':

	# Make a game instance, and run the game
	ai = AlienInvasion()
	ai.run_game()

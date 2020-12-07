import pygame
import sys
from settings import *
from player_class import *
from enemy_class import *

# initializing pygame module
pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PACMAN GAME")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.coins = []
        self.s_coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

############################ HELPER FUNCTIONS ##################################
	
	#Draw text function to write text on screen
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    # load function to load maze.
    def load(self):
        self.background = pygame.image.load('Assets/maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Opening Wall file
        # Creating Wall list with co-ordinates of walls
        # stored as  a vector
        with open("Wall.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":									# 1 = Wall
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":								# C = Coins / Points
                        self.coins.append(vec(xidx, yidx))
                    elif char == "S":								# S = Special Coins / Points +10
                        self.s_coins.append(vec(xidx, yidx))
                    elif char == "P":								# P = Initial position of Player
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:				# Initial Position of Enemys
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height, self.cell_width, self.cell_height))
	
    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

	#Reset game after end of game if user enters space
    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        self.s_coins = []
        with open("Wall.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
                    if char == 'S':
                        self.s_coins.append(vec(xidx, yidx))
        self.state = "playing"


########################### STARTING FUNCTIONS ####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        
        #Designing attractive starting screen
        self.draw_text('PA  MAN', self.screen, [WIDTH//2, HEIGHT//2-250], 100, WHITE, START_FONT, centered=True)
        ghost = pygame.image.load('Assets/pacman01.png')
        ghost = pygame.transform.scale(ghost, (65,80))
        self.screen.blit(ghost, (WIDTH//2-90, HEIGHT//2-285, 65, 80))
                       
        self.draw_text('CHARACTER  /  NICNAME', self.screen, [WIDTH//2, HEIGHT//2-80], 28, WHITE, START_FONT, centered=True)
        #RED Enemy
        self.draw_text('SHADOW         "BLINKY"', self.screen, [WIDTH//2-150, HEIGHT//2-45], 25, RED, START_FONT, centered=False)
        ghost = pygame.image.load('Assets/ghost01.png')
        ghost = pygame.transform.scale(ghost, (int(SQUARE), int(SQUARE)))
        self.screen.blit(ghost, (WIDTH//2-225, HEIGHT//2-35, SQUARE, SQUARE))
        #PINK Enemy
        self.draw_text('SPEEDY           "PINKY"', self.screen, [WIDTH//2-150, HEIGHT//2-15], 25, PINK, START_FONT, centered=False)
        ghost = pygame.image.load('Assets/ghost02.png')
        ghost = pygame.transform.scale(ghost, (int(SQUARE), int(SQUARE)))
        self.screen.blit(ghost, (WIDTH//2-225, HEIGHT//2-5, SQUARE, SQUARE))
        #BLUE Enemy
        self.draw_text('BASHFUL        "INKY"', self.screen, [WIDTH//2-150, HEIGHT//2+15], 25, CYAN, START_FONT, centered=False)
        ghost = pygame.image.load('Assets/ghost03.png')
        ghost = pygame.transform.scale(ghost, (int(SQUARE), int(SQUARE)))
        self.screen.blit(ghost, (WIDTH//2-225, HEIGHT//2+25, SQUARE, SQUARE))
        #ORANGE Enemy
        self.draw_text('POKEY            "CLYDE"', self.screen, [WIDTH//2-150, HEIGHT//2+45], 25, ORANGE, START_FONT, centered=False)
        ghost = pygame.image.load('Assets/ghost04.png')
        ghost = pygame.transform.scale(ghost, (int(SQUARE), int(SQUARE)))
        self.screen.blit(ghost, (WIDTH//2-225, HEIGHT//2+55, SQUARE, SQUARE))

        self.draw_text('PUSH SPACE TO PLAY', self.screen, [WIDTH//2, HEIGHT-50], 27, GREY, START_FONT, centered=True)
                       
        #Enemys Character and Nicname on starting screen
        ghost = pygame.image.load('Assets/ghost01.png')
        ghost = pygame.transform.scale(ghost, (30, 30))
        self.screen.blit(ghost, (WIDTH//2-200, HEIGHT-180, 30, 30))
        ghost = pygame.image.load('Assets/ghost02.png')
        ghost = pygame.transform.scale(ghost, (30, 30))
        self.screen.blit(ghost, (WIDTH//2-150, HEIGHT-180, 30, 30))
        ghost = pygame.image.load('Assets/ghost03.png')
        ghost = pygame.transform.scale(ghost, (30, 30))
        self.screen.blit(ghost, (WIDTH//2-100, HEIGHT-180, 30, 30))
        ghost = pygame.image.load('Assets/ghost04.png')
        ghost = pygame.transform.scale(ghost, (30, 30))
        self.screen.blit(ghost, (WIDTH//2-50, HEIGHT-180, 30, 30))
        ghost = pygame.image.load('Assets/pacman01.png')
        ghost = pygame.transform.scale(ghost, (30, 30))
        self.screen.blit(ghost, (WIDTH//2+70, HEIGHT-180, 30, 30))
        pygame.draw.circle(self.screen, YELLOW,(WIDTH//2+115,HEIGHT-165), 5)
        pygame.draw.circle(self.screen, YELLOW,(WIDTH//2+135,HEIGHT-165), 5)
        pygame.draw.circle(self.screen, YELLOW,(WIDTH//2+155,HEIGHT-165), 5)
        pygame.draw.circle(self.screen, YELLOW,(WIDTH//2+175,HEIGHT-165), 5)
        pygame.draw.circle(self.screen, YELLOW,(WIDTH//2+195,HEIGHT-165), 5)
        pygame.draw.line(self.screen, BLUE, [0, HEIGHT-150], [WIDTH, HEIGHT-150], 4)
        pygame.draw.line(self.screen, BLUE, [0, HEIGHT-130], [WIDTH, HEIGHT-130], 4)
        
        pygame.display.update()
        
########################### PLAYING FUNCTIONS ##################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [60, 0], 18, WHITE, START_FONT)
        self.draw_text('HIGH SCORE: 200', self.screen, [WIDTH//2+60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    # If player is killed by Emeny
    # Decrease 1 life of Player
    # Total 3 lives ia available
    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
        	# Player / Enemies position will set back to starting position
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    #Drawing coins/point in maze
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (255,244,79),
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 3)
        for s_coin in self.s_coins:
            pygame.draw.circle(self.screen, (255,244,79),
                               (int(s_coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(s_coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

########################### GAME OVER FUNCTIONS ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    # Displaying GAME OVER screen
    def game_over_draw(self):
        self.screen.fill(BLACK) 
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 100],  52, RED, START_FONT, centered=True)
        self.draw_text("PRESS SPACE TO PLAY", self.screen, [WIDTH//2, HEIGHT//2],  30, (190, 190, 190), "arial", centered=True)
        self.draw_text("PRESS ESC TO QUIT", self.screen, [WIDTH//2, HEIGHT//1.5],  30, (190, 190, 190), "arial", centered=True)
        pygame.display.update()










########################### EXTRA FUNCTIONS ################################

''' setting grid of maze as a reference to Player and Enemy
    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))
'''

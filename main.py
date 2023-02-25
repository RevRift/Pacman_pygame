""" 

You are Vax-man

Vax-man is a yellow circle, the ghosts are blue circles
Use arrow keys to move vaxman
At the start, there are 10 ghosts on the board
Ghosts duplicate every 15 seconds
Vax-man can vaccinate (i.e. delete) ghosts
Vax-man can also collect yellow dots

Goal - collect all the dots before the number of ghosts reaches 40

Things to improve:

Making the movement less choppy
Increasing the dimensions of the board
Changing direction has to be timed perfectly otherwise you miss the turn
Adding sounds
Representing Vax-man and the ghosts with images

"""


import pygame, sys
from pygame.math import Vector2
from random import randint
from timeit import default_timer

pygame.init()
pygame.font.init()

# window
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vaxman")

TEXT_FONT = pygame.font.SysFont('comicsans', 25)
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 50)

# settings
FPS = 60
SQUARE_LENGTH = 40  # 15 x 15 grid (resizing will break the game)
PLAYER_VEL = 5
GHOST_VEL = 3

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
PURPLE = (255,0,255)
YELLOW = (255,255,0)
DIRECTIONS = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]

MOVE_PLAYER = pygame.USEREVENT
pygame.time.set_timer(MOVE_PLAYER, int(1000/PLAYER_VEL))
MOVE_GHOSTS = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_GHOSTS, int(1000/GHOST_VEL))
DUPLICATE_GHOSTS = pygame.USEREVENT + 2
pygame.time.set_timer(DUPLICATE_GHOSTS, int(15000)) # 15s

class Player: # represents player(i.e. vax-man), ghosts, and dots
    def __init__(self, x, y, color):
        self.pos = Vector2(x, y)
        self.color = color
        self.direction = Vector2(0, 1)

class Dot:
    def __init__(self, x, y, color):
        self.pos = Vector2(x, y)
        self.color = color

class Wall: # black rectangles neither players nor ghost can cross
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x * SQUARE_LENGTH, y * SQUARE_LENGTH, 
                width * SQUARE_LENGTH, height * SQUARE_LENGTH)

# set up entities
player = Player(0, 0, YELLOW)
score = 0
ghosts = []
dots = []
WALLS = []
JUNCTIONS = []

# set up grid
# note: grid.txt contains the original map layout
# 0 = wall, 1 = dot, 2 = ghost
grid = open('grid.txt', 'r')
for y, line in enumerate(grid):
    for x, char in enumerate(line): # make an assertion that the dimensions are correct
        if char == '0':
            WALLS.append(Wall(x, y, 1, 1))
        elif char == '1':
            dots.append(Dot(x, y, YELLOW))

        elif char == '2':
            ghosts.append(Player(x, y, BLUE))
grid.close()


def draw_window():

    WIN.fill(BLACK)

    for wall in WALLS:
        pygame.draw.rect(WIN, GREEN, wall.rect)

    for dot in dots:
        pygame.draw.circle(WIN, dot.color, 
                    (int(dot.pos.x * SQUARE_LENGTH + SQUARE_LENGTH/2), 
                     int(dot.pos.y * SQUARE_LENGTH + SQUARE_LENGTH/2)), 
                     5)

    for ghost in ghosts:
        pygame.draw.circle(WIN, ghost.color, 
                        (int(ghost.pos.x * SQUARE_LENGTH + SQUARE_LENGTH/2), 
                        int(ghost.pos.y * SQUARE_LENGTH + SQUARE_LENGTH/2)), 
                        int(SQUARE_LENGTH/2 - SQUARE_LENGTH/10))

    pygame.draw.circle(WIN, player.color, 
                    (int(player.pos.x * SQUARE_LENGTH + SQUARE_LENGTH/2), 
                     int(player.pos.y * SQUARE_LENGTH + SQUARE_LENGTH/2)), 
                     int(SQUARE_LENGTH/2 - SQUARE_LENGTH/10))

    ghost_count_text = TEXT_FONT.render("Ghost count: " + str(len(ghosts)), 1, WHITE)
    WIN.blit(ghost_count_text, (10 * SQUARE_LENGTH - ghost_count_text.get_width() - 10, 
                            6 * SQUARE_LENGTH - ghost_count_text.get_height() - 10))

    score_text = TEXT_FONT.render("Score: " + str(score), 1, WHITE)
    WIN.blit(score_text, (10 * SQUARE_LENGTH - score_text.get_width() - 10, 
                        10 * SQUARE_LENGTH - score_text.get_height() - 10))

    pygame.display.update() 


def will_collide(object, direction):
    next_rect = pygame.Rect(((object.pos.x + direction.x) % 15) * SQUARE_LENGTH, 
                            ((object.pos.y + direction.y) % 15) * SQUARE_LENGTH, 
                            SQUARE_LENGTH, SQUARE_LENGTH)
    return any(next_rect.colliderect(wall.rect) for wall in WALLS)

def rand_direction(ghost):

    directions = DIRECTIONS[:]

    # if ghost will collide, change it's direction
    if will_collide(ghost, ghost.direction):
        new_direction = directions[randint(0, len(directions)-1)]
        while will_collide(ghost, new_direction):
            new_direction = directions[randint(0, len(directions)-1)]
        return new_direction
    
    # ghost will sometimes turn at junctions (note: i forgot to add the junctions at Vector(0, 0) and in all of the first and last row)
    if ghost.pos == Vector2(3, 2):
        directions.remove(Vector2(0, 1))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(5, 2):
        directions.remove(Vector2(0, 1))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(9, 2):
        directions.remove(Vector2(0, 1))
        return directions[randint(0, len(directions)-1)]           
    elif ghost.pos == Vector2(11, 2):
        directions.remove(Vector2(0, 1))
        return directions[randint(0, len(directions)-1)]

    elif ghost.pos == Vector2(3, 12):
        directions.remove(Vector2(0, -1))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(5, 12):
        directions.remove(Vector2(0, -1))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(9, 12):
        directions.remove(Vector2(0, -1))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(11, 12):
        directions.remove(Vector2(0, -1))
        return directions[randint(0, len(directions)-1)]
    
    elif ghost.pos == Vector2(7, 4):
        directions.remove(Vector2(0, 1))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(7, 10):
        directions.remove(Vector2(0, -1))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(7, 2):
        directions.remove(Vector2(0, -1))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(7, 12):
        directions.remove(Vector2(0, 1))
        return directions[randint(0, len(directions)-1)]

    elif ghost.pos == Vector2(2, 7):
        directions.remove(Vector2(1, 0))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(12, 7):
        directions.remove(Vector2(-1, 0))
        return directions[randint(0, len(directions)-1)]

    elif ghost.pos == Vector2(4, 4):
        directions.remove(Vector2(0, -1))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(4, 10):
        directions.remove(Vector2(0, -1))
        return directions[randint(0, len(directions)-1)]

    elif ghost.pos == Vector2(2, 4):
        directions.remove(Vector2(-1, 0))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(12, 4):
        directions.remove(Vector2(1, 0))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(2, 10):
        directions.remove(Vector2(-1, 0))
        return directions[randint(0, len(directions)-1)]
    elif ghost.pos == Vector2(12, 10):
        directions.remove(Vector2(1, 0))
        return directions[randint(0, len(directions)-1)]
    
    # if not at an intersection, the ghost will continue in the same direction
    return ghost.direction

def player_at_ghost():
    for ghost in ghosts:
        if player.pos == ghost.pos:
            ghosts.remove(ghost)
            return True
    
    return False

def player_at_dot():
    for dot in dots:
        if player.pos == dot.pos:
            dots.remove(dot)
            return True
    
    return False

def main():
    
    global player, ghosts, score
    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True   # I know there's no point in this if i'm returning right after...
                return

            if event.type == MOVE_PLAYER and not will_collide(player, player.direction):
                x = (player.pos.x + player.direction.x) % 15             
                y = (player.pos.y + player.direction.y) % 15                 
                player.pos = Vector2(x, y)
            
            if event.type == MOVE_GHOSTS:
                for ghost in ghosts:                   
                    ghost.direction = rand_direction(ghost)
                    x = (ghost.pos.x + ghost.direction.x) % 15             
                    y = (ghost.pos.y + ghost.direction.y) % 15                 
                    ghost.pos = Vector2(x, y)
            
            if player_at_ghost():
                score += 10
            
            if player_at_dot():
                score += 1
            
            if event.type == DUPLICATE_GHOSTS:
                ghost_count = len(ghosts)
                for i in range(ghost_count):
                    new_ghost = Player(ghosts[i].pos.x, ghosts[i].pos.y, ghosts[i].color)
                    ghosts.append(new_ghost)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not will_collide(player, Vector2(-1, 0)):
                    player.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and not will_collide(player, Vector2(1, 0)):
                    player.direction = Vector2(1, 0)
                if event.key == pygame.K_UP and not will_collide(player, Vector2(0, -1)):
                    player.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and not will_collide(player, Vector2(0, 1)):
                    player.direction = Vector2(0, 1)
                
        draw_window()

        if len(dots) == 0:
            win_text = GAME_OVER_FONT.render("YOU WIN", 1, WHITE)
            WIN.blit(win_text, (WIDTH/2 - win_text.get_width()//2, HEIGHT/2 - win_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            game_over = True   # or i could just return but it's cooler this way
        elif len(ghosts) >= 50:
            lose_text = GAME_OVER_FONT.render("YOU LOSE", 1, RED)
            WIN.blit(lose_text, (WIDTH/2 - lose_text.get_width()//2, HEIGHT/2 - lose_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            game_over = True


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
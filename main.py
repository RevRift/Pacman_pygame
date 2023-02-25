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

# note: grid.txt displays the original map layout
# 0 = wall, 1 = dot, 2 = ghost
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

player = Player(0, 0, YELLOW)
score = 0
ghosts = [
    Player(11, 0, BLUE),
    Player(2, 10, BLUE),
    Player(10, 7, BLUE),
    Player(7, 4, BLUE),
    Player(9, 12, BLUE),
    Player(11, 0, BLUE),
    Player(2, 10, BLUE),
    Player(10, 7, BLUE),
    Player(7, 4, BLUE),
    Player(9, 12, BLUE)
]



WALLS = [ 
# (x, y, width, height)
    Wall(1, 1, 2, 1),
    Wall(1, 2, 1, 5),
    Wall(1, 8, 1, 5),
    Wall(1, 13, 2, 1),
    Wall(4, 0, 1, 2),
    Wall(10, 0, 1, 2),
    Wall(6, 1, 3, 1),
    Wall(3, 3, 4, 1),
    Wall(8, 3, 4, 1),
    Wall(3, 5, 1, 5),
    Wall(5, 5, 5, 5),
    Wall(11, 5, 1, 5),
    Wall(3, 11, 4, 1),
    Wall(8, 11, 4, 1),
    Wall(4, 13, 1, 2),
    Wall(10, 13, 1, 2),
    Wall(6, 13, 3, 1),
    Wall(12, 1, 2, 1),
    Wall(13, 2, 1, 5),
    Wall(13, 8, 1, 5),
    Wall(12, 13, 2, 1)
]

dots = [
    Dot(0, 0, YELLOW),
    Dot(0, 1, YELLOW),
    Dot(0, 2, YELLOW),
    Dot(0, 3, YELLOW),
    Dot(0, 4, YELLOW),
    Dot(0, 5, YELLOW),
    Dot(0, 6, YELLOW),
    Dot(0, 7, YELLOW),
    Dot(0, 8, YELLOW),
    Dot(0, 9, YELLOW),
    Dot(0, 10, YELLOW),
    Dot(0, 11, YELLOW),
    Dot(0, 12, YELLOW),
    Dot(0, 13, YELLOW),
    Dot(0, 14, YELLOW),
    Dot(1, 0, YELLOW),
    Dot(1, 0, YELLOW),
    Dot(1, 7, YELLOW),
    Dot(1, 14, YELLOW),
    Dot(2, 0, YELLOW),
    Dot(2, 2, YELLOW),
    Dot(2, 3, YELLOW),
    Dot(2, 4, YELLOW),
    Dot(2, 5, YELLOW),
    Dot(2, 6, YELLOW),
    Dot(2, 7, YELLOW),
    Dot(2, 8, YELLOW),
    Dot(2, 9, YELLOW),
    Dot(2, 10, YELLOW),
    Dot(2, 11, YELLOW),
    Dot(2, 12, YELLOW),
    Dot(2, 14, YELLOW),
    Dot(3, 0, YELLOW),
    Dot(3, 1, YELLOW),
    Dot(3, 2, YELLOW),
    Dot(3, 4, YELLOW),
    Dot(3, 10, YELLOW),
    Dot(3, 12, YELLOW),
    Dot(3, 13, YELLOW),
    Dot(3, 14, YELLOW),
    Dot(4, 2, YELLOW),
    Dot(4, 4, YELLOW),
    Dot(4, 5, YELLOW),
    Dot(4, 6, YELLOW),
    Dot(4, 7, YELLOW),
    Dot(4, 8, YELLOW),
    Dot(4, 9, YELLOW),
    Dot(4, 10, YELLOW),
    Dot(4, 12, YELLOW),
    Dot(5, 0, YELLOW),
    Dot(5, 1, YELLOW),
    Dot(5, 2, YELLOW),
    Dot(5, 4, YELLOW),
    Dot(5, 10, YELLOW),
    Dot(5, 12, YELLOW),
    Dot(5, 13, YELLOW),
    Dot(5, 14, YELLOW),
    Dot(6, 0, YELLOW),
    Dot(6, 2, YELLOW),
    Dot(6, 4, YELLOW),
    Dot(6, 10, YELLOW),
    Dot(6, 12, YELLOW),
    Dot(6, 14, YELLOW),
    Dot(7, 0, YELLOW),
    Dot(7, 2, YELLOW),
    Dot(7, 3, YELLOW),
    Dot(7, 4, YELLOW),
    Dot(7, 10, YELLOW),
    Dot(7, 11, YELLOW),
    Dot(7, 12, YELLOW),
    Dot(7, 14, YELLOW),
    Dot(8, 0, YELLOW),
    Dot(8, 2, YELLOW),
    Dot(8, 4, YELLOW),
    Dot(8, 10, YELLOW),
    Dot(8, 12, YELLOW),
    Dot(8, 14, YELLOW),
    Dot(9, 0, YELLOW),
    Dot(9, 1, YELLOW),
    Dot(9, 2, YELLOW),
    Dot(9, 4, YELLOW),
    Dot(9, 10, YELLOW),
    Dot(9, 12, YELLOW),
    Dot(9, 13, YELLOW),
    Dot(9, 14, YELLOW),
    Dot(10, 2, YELLOW),
    Dot(10, 4, YELLOW),
    Dot(10, 5, YELLOW),
    Dot(10, 6, YELLOW),
    Dot(10, 7, YELLOW),
    Dot(10, 8, YELLOW),
    Dot(10, 9, YELLOW),
    Dot(10, 10, YELLOW),
    Dot(10, 12, YELLOW),
    Dot(11, 0, YELLOW),
    Dot(11, 1, YELLOW),
    Dot(11, 2, YELLOW),
    Dot(11, 4, YELLOW),
    Dot(11, 10, YELLOW),
    Dot(11, 12, YELLOW),
    Dot(11, 13, YELLOW),
    Dot(11, 14, YELLOW),
    Dot(12, 0, YELLOW),
    Dot(12, 2, YELLOW),
    Dot(12, 3, YELLOW),
    Dot(12, 4, YELLOW),
    Dot(12, 5, YELLOW),
    Dot(12, 6, YELLOW),
    Dot(12, 7, YELLOW),
    Dot(12, 8, YELLOW),
    Dot(12, 9, YELLOW),
    Dot(12, 10, YELLOW),
    Dot(12, 11, YELLOW),
    Dot(12, 12, YELLOW),
    Dot(12, 14, YELLOW),
    Dot(13, 0, YELLOW),
    Dot(13, 0, YELLOW),
    Dot(13, 7, YELLOW),
    Dot(13, 14, YELLOW),
    Dot(14, 0, YELLOW),
    Dot(14, 1, YELLOW),
    Dot(14, 2, YELLOW),
    Dot(14, 3, YELLOW),
    Dot(14, 4, YELLOW),
    Dot(14, 5, YELLOW),
    Dot(14, 6, YELLOW),
    Dot(14, 7, YELLOW),
    Dot(14, 8, YELLOW),
    Dot(14, 9, YELLOW),
    Dot(14, 10, YELLOW),
    Dot(14, 11, YELLOW),
    Dot(14, 12, YELLOW),
    Dot(14, 13, YELLOW),
    Dot(14, 14, YELLOW)
# don't ask how long this took
]

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


def will_collide(circle, direction):
    next_rect = pygame.Rect(((circle.pos.x + direction.x) % 15) * SQUARE_LENGTH, 
                            ((circle.pos.y + direction.y) % 15) * SQUARE_LENGTH, 
                            SQUARE_LENGTH, SQUARE_LENGTH)
    for wall in WALLS:                   
        if next_rect.colliderect(wall.rect):
            return True

    return False

def rand_direction(ghost):

    directions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
    rand_direction = rand_direction = directions[randint(0, len(directions)-1)]

    if will_collide(ghost, ghost.direction):
        ghost.direction = rand_direction
        while will_collide(ghost, rand_direction):
            rand_direction = directions[randint(0, len(directions)-1)]
    else:
        # ghost will sometimes turn at intersections       
        if randint(0, 1): 
            return ghost.direction

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

        else:
            return ghost.direction
    
    return rand_direction

def player_at_ghost():
    for ghost in ghosts:
        if player.pos.x == ghost.pos.x and player.pos.y == ghost.pos.y:
            ghosts.remove(ghost)
            return True
    
    return False

def player_at_dot():
    for dot in dots:
        if player.pos.x == dot.pos.x and player.pos.y == dot.pos.y:
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
            
            # if event.type == DUPLICATE_GHOSTS:
            #     ghost_count = len(ghosts)
            #     for i in range(ghost_count):
            #         new_ghost = Circle(ghosts[i].pos.x, ghosts[i].pos.y, ghosts[i].color)
            #         ghosts.append(new_ghost)
            
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
        elif len(ghosts) >= 40:
            lose_text = GAME_OVER_FONT.render("YOU LOSE", 1, RED)
            WIN.blit(lose_text, (WIDTH/2 - lose_text.get_width()//2, HEIGHT/2 - lose_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            game_over = True


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
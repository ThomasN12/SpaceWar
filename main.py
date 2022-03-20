import pygame
import os #Operating system => help define the path to images
pygame.font.init() #Initialize pygame font library

WIDTH, HEIGHT = 900, 500 # Capital to define constant
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LOL")   #Game title
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)      #Declare the used font
WINNER_FONT = pygame.font.SysFont('conmicans', 50)
FPS = 60
VEL = 5
BULLET_VEL = 7
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2
BORDER = pygame.Rect(WIDTH/2-5,0,10,500)
MAX_BULLET = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)  #Resize the spaceship
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'spaceship_red.png')), 270)
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) #Pause for 5 seconds

def draw_window(yellow, red, yellow_bullet, red_bullet, yellow_health, red_health):
    yellow_health_text = HEALTH_FONT.render('Health:' + str(yellow_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render('Health:' + str(red_health), 1, WHITE)
    WIN.blit(BACKGROUND_IMAGE, (0,0))         #A background is drawn every SINGLE FRAME
    pygame.draw.rect(WIN, BLACK, BORDER)    #Draw the black border on the window
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))   #Draw on the SURFACE of the screen, and from the TOP LEFT
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) 
    WIN.blit(yellow_health_text, (0,0))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 0))
    for bullet in yellow_bullet:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullet:
        pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update() #Update what we draw on the window

def yellow_function_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL >= 0:     #Left, if key pressed == a
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x :     #Right, if key pressed == d
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL >= 0:
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL
def red_function_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:     #Left, if key pressed == LEFT
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:     #Right, if key pressed == RIGHT
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:
        red.y += VEL

def handle_bullet(yellow, red, yellow_bullet, red_bullet):
    for bullet in yellow_bullet:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))      #???
            yellow_bullet.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullet.remove(bullet)
    
    for bullet in red_bullet:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))          #???
            red_bullet.remove(bullet)
        elif bullet.x < 0:
            red_bullet.remove(bullet)


def main():
    run = True
    clock = pygame.time.Clock()
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  #location to draw the spaceship
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullet = []      #List of RECTANGLE bullets
    red_bullet = []
    red_health = 10
    yellow_health = 10
    #while-loop keeps the game open
    while run:
        clock.tick(FPS)    #the loop win run 'FPS' times per second
        for event in pygame.event.get():    #list of different events
            if event.type == pygame.QUIT:   #Click 'X' = pygame.QUIT => quit
                pygame.quit()
            
            if event.type == pygame.KEYDOWN: #Check if the key is pressed down or not
                if event.key == pygame.K_LCTRL and len(yellow_bullet) < MAX_BULLET:
                    yBullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 4)
                    yellow_bullet.append(yBullet)
                if event.key == pygame.K_RCTRL and len(red_bullet) < MAX_BULLET:
                    rBullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 4)
                    red_bullet.append(rBullet)
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
        if yellow_health <= 0:
            winner_text = "Red wins!"
        if winner_text != "":
            draw_winner(winner_text) #Someone wins and the game ends
            break
        key_pressed = pygame.key.get_pressed()  #The key we are pressing
        yellow_function_movement(key_pressed, yellow)
        red_function_movement(key_pressed, red)
        handle_bullet(yellow, red, yellow_bullet, red_bullet)
        draw_window(yellow, red, yellow_bullet, red_bullet, yellow_health, red_health)
    main()    

        
#Only run the game if run this file directly, not when this file is imported
#__name__ = name of the file
if __name__ == "__main__":   
    main()

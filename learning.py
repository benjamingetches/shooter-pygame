import pygame
import os
pygame.font.init() #inits font lib
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game 1 -ben") #sets our window name


WHITE = (255,255,255)
YELLOWCOLOR = (255,255,0)
REDCOLOR = (255,0,0)
BLACK = (0,0,0)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
RED_WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'red_wins.mp3'))
YELLOW_WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'yellow_wins.mp3'))

BORDER = pygame.Rect(445, 0, 10, HEIGHT)

SHIP_WIDTH, SHIP_HEIGHT = 55, 40 #good practice!!!! do this
FPS = 60
VEL = 5
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(  #rotates img too
    YELLOW_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90) #image resizing, x, y amount
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BULLET_VEL = 8
MAX_BULLETS = 3

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 80)
#####################################





#function to clean up our drawings
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)        
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))#draws a surface on the screen - img, pos
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    



    for bullet in red_bullets:
        pygame.draw.rect(WIN, REDCOLOR, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOWCOLOR, bullet)
    
    
    pygame.display.update()


def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 10:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: 
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 10:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL
    

def handle_bullets(yellow_bullets, red_bullets, yellow, red): #masjor takeaway - use events to mod outside funcs
    #yellows, reds
    for bullet in yellow_bullets:
        #move it, then check it
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)        

def draw_win(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(4000)



def generate_presses(yellow_bullets, red_bullets, yellow, self, next_move):
    # analyze position of enemy (yellow), count of bullets, location of enemy bullets, current position
    # decide if attack is possible, if so, move towards enemy y cord, and decide if firing is good (possible to do, and likely to hit)
    # if not, likely in danger, look to move away from enemy pos/bullets
    # Constants
    THREAT_RADIUS = 300  # Distance within which a bullet is considered a threat
    Y_MARGIN = 60        # Y-axis margin for bullet evasion
    X_MARGIN = 26        # X-axis margin for self

    # Initialize danger level and closest threat
    max_danger = 0
    closest_bullet = None

    # Analyze each bullet to determine the closest and most dangerous threat
    for bullet in yellow_bullets:
        distance = (self.x + X_MARGIN) - (bullet.x + 5)
        y_distance = abs(bullet.y - (20 + self.y))

        if 0 < distance <= THREAT_RADIUS and y_distance < Y_MARGIN:
            danger_level = THREAT_RADIUS - distance  # Higher danger for closer bullets
            if danger_level > max_danger:
                max_danger = danger_level
                closest_bullet = bullet

    #print(next_move)
    if (next_move != 0):
        if(next_move > 0):
            self.y += VEL
            next_move -= 1
        else:
            self.y -= VEL
            next_move += 1

    elif closest_bullet:
        if self.y < 75:
            next_move = 7
            self.y += VEL
        elif self.y > 425:
            next_move = -7
            self.y -= VEL
        else:
            if (self.y + 20) - (closest_bullet.y + 2) < 0:
                self.y -= VEL
            else:
                self.y += VEL
    return next_move
    """danger = -1
    i = 0
    for bullet in yellow_bullets: # danger check
        if((self.x + 26) - (bullet.x + 5) <= 300 and ((self.x + 26) - (bullet.x + 5) > 0) and abs(bullet.y - (20 + self.y)) < 30):
            danger = i
            break
        i = i + 1
    if(danger > -1):
        if(self.y < 50):
            #at top
            self.y += VEL
        elif(self.y > 450):
            # at bottom
            self.y -= VEL
        else:
            incoming = yellow_bullets[i]
            if((self.y + 20) - (incoming.y + 2) < 0):
                self.y -= VEL
            else:
                self.y += VEL"""



def main():
    #define two rects as our red/yellow ship
    red = pygame.Rect(700, 300, SHIP_WIDTH, SHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT)
    #handling bullets
    red_bullets = []
    yellow_bullets = []
    red_health = 7
    yellow_health = 7
    next_move = 0
    #main game loop
    clock = pygame.time.Clock() #sets our game to 60 fps
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            #checks for events occuring in pygame
            #first check: if user quit window
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS: #red bullets
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE.play()

                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS: #yellows
                    bullet = pygame.Rect(yellow.x + yellow.width - 10, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        #handling win cases
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow is the Winner!"
            YELLOW_WIN_SOUND.play()

        if yellow_health <= 0:
            winner_text = "Red is the Winner!"
            RED_WIN_SOUND.play()

        if winner_text != "":
            draw_win(winner_text)
            break 

        #movement for the loop
        keys_pressed = pygame.key.get_pressed() #grabs key presses for every frame
        
        yellow_movement(keys_pressed, yellow)
        next_move = generate_presses(yellow_bullets, red_bullets, yellow, red, next_move)
        handle_bullets(yellow_bullets, red_bullets, yellow, red) #ideas - bullet collision? ammo?


        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health) #yellow on left, red on right
        

    main()

if __name__ == "__main__":
    main()
    #this ensures the game isnt automatically called, 
    # ie we only want to run on this file, not on ones that 
    # import this
            
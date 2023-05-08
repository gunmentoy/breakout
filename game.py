#Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

pygame.init()

#Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (51, 51, 255)
PURPLE = (153, 51, 255)
LIGHTBLUE = (51, 153, 255)

score = 0
lives = 3

#Open a new window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

#Creating game objects
#Paddle
paddle = Paddle(WHITE, 200, 10)
paddle.rect.x = 350
paddle.rect.y = 560

#Ball
ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 400

#Bricks
all_bricks = pygame.sprite.Group()

for i in range(7):
    brick = Brick(PURPLE,80,30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)

for i in range(7):
    brick = Brick(BLUE,80,30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)

for i in range(7):
    brick = Brick(LIGHTBLUE,80,30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

# Add the paddle and the ball to the list of sprites
    all_sprites_list.add(paddle)
    all_sprites_list.add(ball)

# The loop will carry on until the user exits the game (e.g. clicks the close button).
    carryOn = True

# The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done so we exit this loop

    #Moving the paddle when the use uses the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(5)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(5)
        
    #Reset ball and paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        paddle.rect.x = 300
        paddle.rect.y = 560
        ball.rect.x = 400
        ball.rect.y = 550
    

    # --- Game logic
    all_sprites_list.update()

    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x >= 790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 590:
        ball.velocity[1] = -ball.velocity[1]
        lives -= 1
        if lives <= 0:
            #Display Game Over Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (250,300))
            pygame.display.flip()
            pygame.time.wait(3000)

            #Stop the Game
            carryOn=False

    if ball.rect.y < 40:
        ball.velocity[1] = -ball.velocity[1]

    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddle):
      ball.rect.x -= ball.velocity[0]
      ball.rect.y -= ball.velocity[-1]
      ball.bounce()

    #Check if there is the ball collides with any of bricks
    brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
    for brick in brick_collision_list:
      ball.bounce()
      score += 1
      brick.kill()
      if len(all_bricks)==0:
            #Display Level Complete Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            screen.blit(text, (200,300))
            pygame.display.flip()
            pygame.time.wait(3000)

            #Stop the Game
            carryOn = False

    # --- Decorating codes
    #Set screen to black.
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

    #Display the score and the number of lives at the top of the screen.
    font = pygame.font.Font(None, 34)
    text = font.render("Score: " + str(score), 1, WHITE)
    screen.blit(text, (20,10))
    text = font.render("Lives: " + str(lives), 1, WHITE)
    screen.blit(text, (650,10))

    #Draw all the sprites at once.
    all_sprites_list.draw(screen)

    #Update the screen with what has been drawn.
    pygame.display.flip()

    # --- Limit to 60FPS
    clock.tick(60)

#Once exited the main program loop, stop the game engine:
pygame.quit()
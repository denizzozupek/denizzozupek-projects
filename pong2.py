import pygame, random, sys

pygame.init()

#screen settings
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Pongg")

#colors
black = (0,0,0)
white = (255,255,255)

#FPS check - clock
clock = pygame.time.Clock()

ball_speed_x = 6
ball_speed_y = 6
player_speed = 0
cpu_speed = 6

cpu_points , player_points = 0 , 0
score_font = pygame.font.Font(None, 50)

    #game objects
player = pygame.Rect(0,0,20,100)
player.midright = (screen_width, screen_height / 2)

cpu = pygame.Rect(0,0,20,100)
cpu.midleft = (0 , screen_height / 2)

ball = pygame.Rect(0,0,30,30)
ball.center = (screen_width/2, screen_height/2)

def won(winner):
    global cpu_points, player_points
    if winner == "player":
        player_points += 1
    elif winner == "cpu":
        cpu_points += 1
    reset_ball()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width // 2, screen_height //2)
    ball_speed_x = 6 * random.choice([-1,1])
    ball_speed_y = 6 * random.choice([-1,1])
    return ball_speed_x, ball_speed_y

def animate_ball():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.colliderect(player) or ball.colliderect(cpu):
        ball_speed_x *= -1
    if ball.right >= screen_width:
        won("cpu")
    if ball.left <= 0:
        won("player")

def animate_player():
    global player_speed
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def animate_cpu():
    global cpu_speed
    reaction_chance = random.random()

    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height
    if reaction_chance < 0.9:
        if cpu.centery < ball.centery:
            cpu.y += cpu_speed
        elif cpu.centery > ball.centery:
            cpu.y -= cpu_speed


#Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
               player_speed = 0

    animate_ball()
    animate_player()
    animate_cpu()

    screen.fill(black)



    #Draw screen
    pygame.draw.rect(screen, white, player)
    pygame.draw.rect(screen, white, cpu)
    pygame.draw.ellipse(screen, white, ball)

    #Draw Score
    player_score_text = score_font.render(str(player_points), True, "white")
    cpu_score_text = score_font.render(str(cpu_points), True, "white")
    screen.blit(player_score_text, (screen_width/4, 20))
    screen.blit(cpu_score_text, (3* screen_width/4, 20))
    pygame.draw.aaline(screen, 'white', (screen_width/2, 0), (screen_width /2 , screen_height))

    #update screen
    pygame.display.update()
    clock.tick(60) #60 FPS

pygame.quit()
sys.exit()

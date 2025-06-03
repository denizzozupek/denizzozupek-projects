import pygame,random,os,json,sys
pygame.init()
pygame.mixer.init()

#eat sound
eat_sound = pygame.mixer.Sound("pop.wav")

# colors
lightskyblue = (135, 206, 250)
white = (255, 255, 255)
orangered = (255, 69, 0)
brown = (205, 92, 92)
black = (0, 0, 0)

#screen settings
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

#game blocks
cell_size = 20
game_area_x = 50
game_area_y = 50
game_area_size = 700

direction = "RIGHT"
score = 0
high_score = 0
fps = 10  # default FPS

#game fonts
font = pygame.font.SysFont("arial", 24)
title_font = pygame.font.SysFont("arial", 36, bold=True)

#snake body
snake_body = [
    [game_area_x + 3 * cell_size, game_area_y + 5 * cell_size],
    [game_area_x + 2 * cell_size, game_area_y + 5 * cell_size],
    [game_area_x + 1 * cell_size, game_area_y + 5 * cell_size]
]
#food position
def get_random_food_position():
    global snake_body
    x = random.randint(0, (game_area_size - cell_size) // cell_size) * cell_size + game_area_x
    y = random.randint(0, (game_area_size - cell_size) // cell_size) * cell_size + game_area_y
    if [x ,y] not in snake_body:
        return (x,y)
food_position = get_random_food_position()

#score file
def ensure_hs():
    if not os.path.exists("../high_score.json"):
        with open("../high_score.json", "w") as file:
            json.dump({"high_score": 0}, file)
def load_hs():
    with open("../high_score.json", "r") as file:
        return json.load(file)["high_score"]
def save_hs(score):
    with open("../high_score.json", "w") as file:
        json.dump({"high_score": score}, file)
ensure_hs()
high_score = load_hs()

#button rects
start_rect = pygame.Rect(screen_width // 2 - 60, 240, 120, 50)
easy_rect = pygame.Rect(screen_width // 2 - 120, 370, 120, 40)
medium_rect = pygame.Rect(screen_width // 2 + 20, 370, 120, 40)
hard_rect = pygame.Rect(screen_width // 2 - 120, 430, 120, 40)
veryhard_rect = pygame.Rect(screen_width // 2 + 20, 430, 120, 40)
quit_rect = pygame.Rect(screen_width // 2 - 60, 540, 120, 50)
restart_rect = pygame.Rect(screen_width//2-60,340,120,50)
menu_rect   = pygame.Rect(screen_width//2-60,410,120,50)
diff_rect = pygame.Rect(screen_width // 2 - 60 , 300 , 120, 50)

button_color = white
hover_color = (200, 200, 200)
click_color = (150, 150, 150)

def start_game(selected_fps):
    global direction, score, snake_body, food_position, game_state, fps
    fps = selected_fps
    direction = "RIGHT"
    score = 0
    snake_body = [
        [game_area_x + 3 * cell_size, game_area_y + 5 * cell_size],
        [game_area_x + 2 * cell_size, game_area_y + 5 * cell_size],
        [game_area_x + 1 * cell_size, game_area_y + 5 * cell_size]]
    food_position = get_random_food_position()
    game_state = "playing"

def draw_button(rect, text, mouse_pos, mouse_down):
    #click animation
    if rect.collidepoint(mouse_pos):
        color = click_color if mouse_down else hover_color
    else:
        color = button_color
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, black, rect, width=2)
    text_surface = font.render(text, True, black)
    screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2 ,
                               rect.y + (rect.height - text_surface.get_height()) // 2 ))

Running = True
game_state = "menu"

while Running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_down = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        #key controls and manage direction for keys
        if event.type == pygame.KEYDOWN and game_state == "playing":
            if event.key == pygame.K_UP and direction != "DOWN": direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP": direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT": direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT": direction = "RIGHT"

        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "menu":
            if start_rect.collidepoint(mouse_pos):
                start_game(10)
            elif quit_rect.collidepoint(mouse_pos):
                Running = False
            elif easy_rect.collidepoint(mouse_pos):
                start_game(5)
            elif medium_rect.collidepoint(mouse_pos):
                start_game(10)
            elif hard_rect.collidepoint(mouse_pos):
                start_game(20)
            elif veryhard_rect.collidepoint(mouse_pos):
                start_game(30)

            # game-over clicks
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "over":
            if restart_rect.collidepoint(mouse_pos):
                start_game(selected_fps=fps)

        #snake direction
    if game_state == "playing":
        head_x , head_y = snake_body[0]
        if direction == "RIGHT":
            new_head = [head_x + cell_size , head_y]
        elif direction == "LEFT":
            new_head = [head_x - cell_size, head_y]
        elif direction == "UP":
            new_head = [head_x , head_y - cell_size]
        elif direction == "DOWN":
            new_head = [head_x, head_y + cell_size]

        #hit wall - hit yourself control
        if (
            new_head[0] < game_area_x or new_head[0] >= game_area_x + game_area_size or
            new_head[1] < game_area_y or new_head[1] >= game_area_y + game_area_size or new_head in snake_body):
            game_state = "over"

        snake_body.insert(0, new_head)

        #eating the food and growing
        if new_head == list(food_position):
            eat_sound.play()
            score += 1
            if score > high_score:
                high_score = score
                save_hs(high_score)
            food_position = get_random_food_position()
        else:
            snake_body.pop()
    screen.fill(lightskyblue)

    if game_state == "menu":
        title = title_font.render("Snake Game", True, black)
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))
        diff = font.render("Choose Difficulty", True, black)
        screen.blit(diff, (screen_width // 2 - diff.get_width() // 2 , 320))

        # Butonları çiz
        draw_button(start_rect, "Start", mouse_pos, mouse_down)
        draw_button(easy_rect, "Easy", mouse_pos, mouse_down)
        draw_button(medium_rect, "Medium", mouse_pos, mouse_down)
        draw_button(hard_rect, "Hard", mouse_pos, mouse_down)
        draw_button(veryhard_rect, "Very Hard", mouse_pos, mouse_down)
        draw_button(quit_rect, "Quit", mouse_pos, mouse_down)

    elif game_state == "playing":
        # draw food
        pygame.draw.rect(screen, orangered, (food_position[0], food_position[1], cell_size, cell_size))
        # draw game area
        pygame.draw.rect(screen, white, (game_area_x, game_area_y, game_area_size, game_area_size), width=5)
        # draw snake body
        for block in snake_body:
            pygame.draw.rect(screen, brown, (block[0], block[1], cell_size, cell_size))
            pygame.draw.rect(screen, black, (block[0], block[1], cell_size, cell_size), width=1)

        #draw score and name
        title_surface = title_font.render("Snake Game", True , white)
        screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 10))

        score_surface = font.render(f"Score: {score}", True, black)
        screen.blit(score_surface, (game_area_x, game_area_y + game_area_size + 10))

        high_score_surface = font.render(f"High Score: {high_score}", True, black)
        screen.blit(high_score_surface,
                (game_area_x + game_area_size - high_score_surface.get_width(), game_area_y + game_area_size + 10))

    elif game_state == "over":
        game_over = font.render("GAME OVER" ,True, black)
        screen.blit(game_over, (screen_width // 2 - game_over.get_width() // 2, 150))
        score_text = font.render(f"Score: {score}", True, black)
        high_score_text = font.render(f"High score: {high_score}", True, black)
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 220))
        screen.blit(high_score_text, (screen_width // 2 - score_text.get_width() // 2, 260))
        #buttons
        draw_button(restart_rect, "Restart", mouse_pos, mouse_down)
        draw_button(menu_rect, "Menu", mouse_pos, mouse_down)
        draw_button(quit_rect, "Quit", mouse_pos, mouse_down)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if quit_rect.collidepoint(mouse_pos):
            Running = False
        elif menu_rect.collidepoint(mouse_pos):
            game_state = "menu"

    pygame.display.update()
    clock.tick(fps)
pygame.quit()
sys.exit()
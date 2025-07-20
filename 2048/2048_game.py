import pygame, sys, random, os, json

pygame.init()

window_width, window_height = 500, 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("2048")

clock = pygame.time.Clock()
bg_color = (200, 173, 150)
empty_box_color = (210,180,140)
boxes = (238,232,205)

title_colors = {
    2: (254, 243, 214),
    4: (244, 211, 162),
    8: (229, 183, 129),
    16: (255, 139, 0),
    32: (247, 156, 136),
    64: (246, 117, 79),
    128: (254, 245, 128),
    256: (245, 224, 80),
    512: (245, 224, 80),
    1024: (245, 224, 80),
    2048: (245, 224, 80)
}
black_color = (0, 0, 0)
white_color = (255, 255, 255)
font = pygame.font.SysFont("freesansbold", 35)
value_font = pygame.font.SysFont("freesansbold", 45)
title_font =  pygame.font.SysFont("freesansbold", 50)
fps = 60
board_values = [[0 for _ in range(4)] for _ in range(4)]
first_turn = True
spawn_new = False
direction = ""
score = 0
game_over = False

#save high score
def ensure_hs():
    if not os.path.exists("high_score.json"):
        with open("high_score.json", "w") as file:
            json.dump({"high_score": 0}, file)
def load_hs():
    with open("high_score.json", "r") as file:
        return json.load(file)["high_score"]
def save_hs(score):
    with open("high_score.json", "w") as file:
        json.dump({"high_score": score}, file)
ensure_hs()
high_score = load_hs()

def draw_board():
    pygame.draw.rect(window, empty_box_color, (40, 40, 410, 410))
    score_text = font.render(f"Score: {score}", True, black_color)
    high_score_text = font.render(f"High Score: {high_score}", True, black_color)
    title_text = title_font.render("2048", True, black_color)
    title_rect = title_text.get_rect(center=(250, 27))
    window.blit(score_text, ( 50, 460))
    window.blit(high_score_text, (270, 460))
    window.blit(title_text,title_rect)

def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]

            if value == 0:
                color = boxes
            elif value in title_colors:
                color = title_colors[value]
            else:
                color = black_color
            pygame.draw.rect(window,color,[j * 100 + 50, i * 100 + 50, 90, 90], 0, 5)
            pygame.draw.rect(window,black_color, [j * 100 + 50, i * 100 + 50, 90, 90], 2, 5)

            if value != 0:
                value_text = value_font.render(str(value), True, white_color if value >= 8 else black_color)
                text_rect = value_text.get_rect(center = (j * 100 + 95, i * 100 + 95))
                window.blit(value_text, text_rect)

def new_pieces(board):
    empty_cells = [(i,j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
      row, col = random.choice(empty_cells)
      board[row][col] = 4 if random.randint(1,10) == 10 else 2

def move_boxes(direction, board):
    global score
    if direction == "UP":
        for j in range(4):
            values = [board[i][j] for i in range(4) if board[i][j] !=0]

            i = 0
            while i < len(values) - 1:
                if values[i] == values[i+1]:
                    values[i] *= 2
                    score += values[i]
                    values.pop(i+1)
                    i += 1
                else:
                    i += 1
            for i in range(4):
                board[i][j] = values[i] if i < len(values) else 0
        return board

    elif direction == "DOWN":
        for j in range(4):
            values = [board[i][j] for i in range(3, -1, -1) if board[i][j] !=0]

            i = 0
            while i < len(values) - 1:
                if values[i] == values[i+1]:
                    values[i] *= 2
                    score += values[i]
                    values.pop(i+1)
                    i += 1
                else:
                    i += 1
            for i in range(4):
                if i < len(values):
                    board[3 - i][j] = values[i]
                else:

                    board[3 - i][j] = 0
        return board

    elif direction == "LEFT":
        for i in range(4):
            values = [board[i][j] for j in range(4) if board[i][j] !=0]

            #here we are using variable name ik because of i(row) we cant use i
            ik = 0
            while ik < len(values) - 1:
                if values[ik] == values[ik+1]:
                    values[ik] *= 2
                    score += values[ik]
                    values.pop(ik+1)
                    ik += 1
                else:
                    ik += 1
            for j in range(4):
                board[i][j] = values[j] if j < len(values) else 0
        return board

    elif direction == "RIGHT":
        for i in range(4):
            values = [board[i][j] for j in range(3, -1, -1) if board[i][j] != 0]

            ik = 0
            while ik < len(values) - 1:
                if values[ik] == values[ik + 1]:
                    values[ik] *= 2
                    score += values[ik]
                    values.pop(ik + 1)
                    ik += 1
                else:
                    ik += 1
            for j in range(4):
                if j < len(values):
                    board[i][3-j] = values[j]
                else:
                    board[i][3-j] = 0
        return board

def is_game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
    return True

def draw_over():
    pygame.draw.rect(window, black_color, [70, 150, 360, 120], 0, 10)
    game_over_text1 = font.render("Game Over!", True, white_color)
    game_over_text2 = font.render("Press Enter to Restart", True, white_color)
    window.blit(game_over_text1, (180, 170))
    window.blit(game_over_text2, (100, 210))

Run = True
while Run:
    window.fill(bg_color)
    clock.tick(fps)
    draw_board()
    draw_pieces(board_values)

    if first_turn:
        new_pieces(board_values)
        new_pieces(board_values)
        first_turn = False
    elif spawn_new:
        new_pieces(board_values)
        spawn_new = False

    if direction != "":
        board_values = move_boxes(direction, board_values)
        direction = ""
        spawn_new = True

        if is_game_over(board_values):
            game_over = True

    if game_over:
        draw_over()

    if score > high_score:
        high_score = score
        save_hs(score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = "UP"
            elif event.key == pygame.K_DOWN:
                direction = "DOWN"
            elif event.key == pygame.K_LEFT:
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                direction = "RIGHT"

            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    score = 0
                    direction = ""
                    game_over = False
                    first_turn = True

    pygame.display.update()


pygame.quit()
sys.exit()
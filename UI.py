import pygame
from Score import Score

BACKGROUND = "#b0b0b0"
BACKGROUND1 = "#63666A"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255 , 100 , 180)
GRAY = (120, 114, 118)
CELL_COLOR = (153, 156, 158)
BAR = (136, 138, 140)
LINE_WIDTH = 5
DISPLAY_BORDER = 100
DISPLAY_CELL_DIMENSIONS = (100,100)
GRID = pygame.Surface((1200, 800), pygame.SRCALPHA)
image_assets = [
    "magician.png",
    "vaccinated.png",
    "witch.png",
]

# Initialize pygame
pygame_icon = pygame.image.load('Assets/hat.png')
pygame.display.set_icon(pygame_icon)
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Abracadabra!")
pygame.font.init()
game_window_dimensions = (1400, 800)
magician_dimensions = (20, 60)
pygame.display.set_caption("Abracadabra!")
screen.fill(BACKGROUND)
board = None  

def get_action(GameBoard, pixel_x, pixel_y):
    if pixel_x > DISPLAY_BORDER and pixel_y > DISPLAY_BORDER: 
        board_x = int((pixel_x - DISPLAY_BORDER) / DISPLAY_CELL_DIMENSIONS[0])
        board_y = int((pixel_y - DISPLAY_BORDER) / DISPLAY_CELL_DIMENSIONS[1])
        if (board_x >= 0 and board_x < GameBoard.columns and board_y >= 0 and board_y < GameBoard.rows):
            return (board_y, board_x)
    return None

def run(GameBoard):
    screen.fill(BACKGROUND1)
    pygame.draw.rect(screen, BAR, (750, 100, 350, 600))
    build_grid(GameBoard, False)
    display_buttons()
    display_people(GameBoard)      

def display_buttons():
    display_image(screen, "Assets/hat.png", (100,100), (880, 180)) 
    display_image(screen, "Assets/wand.png", (100,100), (880, 400)) 
    my_font = pygame.font.Font("Assets/Minecraft.ttf", 30)
    vanish_text = my_font.render("VANISH", True, (220, 223, 224))
    transform_text = my_font.render("TRANSFORM", True, (220, 223, 224))
    screen.blit(vanish_text, (880, 280))
    screen.blit(transform_text, (840, 500))

def get_events():
    return pygame.event.get()

def display_image(screen, itemStr, dimensions, position):
    v = pygame.image.load(itemStr).convert_alpha()    
    if len(dimensions) != 0:
        v = pygame.transform.scale(v, dimensions)
    screen.blit(v, position)

def build_grid(GameBoard, hasHospital):
    grid_width = GameBoard.columns * DISPLAY_CELL_DIMENSIONS[0]
    grid_height = GameBoard.rows * DISPLAY_CELL_DIMENSIONS[1]
    pygame.draw.rect(screen, BLACK, [DISPLAY_BORDER - LINE_WIDTH, DISPLAY_BORDER - LINE_WIDTH, LINE_WIDTH, grid_height + (2 * LINE_WIDTH)])  # left
    pygame.draw.rect(screen, BLACK, [DISPLAY_BORDER + grid_width, DISPLAY_BORDER - LINE_WIDTH, LINE_WIDTH, grid_height + (2 * LINE_WIDTH)])  # right
    pygame.draw.rect(screen, BLACK, [DISPLAY_BORDER - LINE_WIDTH, DISPLAY_BORDER + grid_height, grid_width + (2 * LINE_WIDTH), LINE_WIDTH])  # bottom
    pygame.draw.rect(screen, BLACK, [DISPLAY_BORDER - LINE_WIDTH, DISPLAY_BORDER - LINE_WIDTH, grid_width + (2 * LINE_WIDTH), LINE_WIDTH])   # top
    pygame.draw.rect(screen, CELL_COLOR, [DISPLAY_BORDER, DISPLAY_BORDER, grid_width, grid_height]) # Fill the inside wioth the cell color

    v = pygame.image.load("Assets/background.jpeg").convert_alpha()
    GRID.blit(v, (0, 0))    

    GRID.set_alpha(128)
    i = DISPLAY_BORDER + DISPLAY_CELL_DIMENSIONS[0]
    while i < DISPLAY_BORDER + grid_width:
        pygame.draw.rect(GRID, GRAY, [i, DISPLAY_BORDER, LINE_WIDTH, grid_height])
        i += DISPLAY_CELL_DIMENSIONS[0]
    i = DISPLAY_BORDER + DISPLAY_CELL_DIMENSIONS[1]
    while i < DISPLAY_BORDER + grid_height:
        pygame.draw.rect(GRID, GRAY, [DISPLAY_BORDER, i, grid_width, LINE_WIDTH])
        i += DISPLAY_CELL_DIMENSIONS[1]
    screen.blit(GRID, (0,0))

def display_people(GameBoard):
    for r in range(GameBoard.rows):
        for c in range(GameBoard.columns):
            if GameBoard.states[r][c] is not None:
                p = GameBoard.states[r][c]
                char = "Assets/" + image_assets[0]
                if p.isVaccinated:
                    char = "Assets/" + image_assets[1]
                elif p.iswitch:
                    char = "Assets/" + image_assets[2]
                coords = (
                    c * DISPLAY_CELL_DIMENSIONS[1] + DISPLAY_BORDER + 10,
                    r * DISPLAY_CELL_DIMENSIONS[0] + DISPLAY_BORDER + 10,
                )
                display_image(screen, char, (80, 80), coords)

def display_win_screen(num_magicians, score, times, bonus):
    screen.fill("#C4A484")
    BACKGROUND2 = "#C4A484"
    GOLD = "#FFD700"
    my_font = pygame.font.Font("Assets/Minecraft.ttf", 32)
    pygame.draw.rect(screen, BLACK, (250, 400, 700, 350))
    pygame.draw.rect(screen, BLACK, (450, 350, 300, 50))
    screen.blit(
        pygame.font.SysFont("Calibri", 32).render(f"You win! You now have {num_magicians} magicians!", True, WHITE),
        (300, 200),
    )
    screen.blit(
        pygame.font.SysFont("Calibri", 32).render(f"You vanished {Score.witches_killed} witches.", True, WHITE),
        (75, 250),
    )
    screen.blit(
        my_font.render(f"RESULT", True, GOLD),
        (540, 360),
    )
    screen.blit(
        my_font.render(f"Calculating Score...", True, WHITE),
        (300, 450),
    )

    screen.blit(
    my_font.render(f"RESULT", True, GOLD),
    (540, 360),
    ) 
    screen.blit(
        my_font.render(f"MISSION SCORE: {score}", True, GOLD),
        (300, 500),
    )
    screen.blit(
        my_font.render(f"TIME BONUS: {times}", True, GOLD),
        (300, 550),
    )
    screen.blit(
    my_font.render(f"SURVIVOR BONUS: {bonus}", True, GOLD),
    (300, 600),
    )
    screen.blit(
        my_font.render(f"TOTAL: {bonus+score+times}", True, GOLD),
        (300, 700),
    )
    pygame.display.update()
    pygame.time.wait(100000)
    pygame.quit()

def display_lose_screen(num_witches):
    screen.fill(BACKGROUND)
    screen.blit(
        pygame.font.SysFont("Minecraft.ttf", 36).render(f"You lose! There were {num_witches} witches when the game ended", True, WHITE),
        (300, 500),
    )

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return

def display_start_screen(starthover):
    screen.fill(BACKGROUND1)
    #screen.wrapper(ascii)
    display_image(screen, "Assets/Video.gif", (1200, 800), (0,0))
    my_font = pygame.font.Font("Assets/Minecraft.ttf", 100)
    text_image = my_font.render("Abracadabra", True, WHITE)
    screen.blit(
         text_image, (275, 100),
    )
    if starthover == "start":
        display_image(screen, "Assets/start_img_2.png", (400, 200), (400, 600))
    else:
        display_image(screen, "Assets/start_img.png", (400, 200), (400, 600))
    pygame.display.update()

def select(coord):
    left = coord[1] * 100 + 100
    top = coord[0] * 100 + 100
    color = (232, 232, 232)
    pygame.draw.rect(screen, color, pygame.Rect(left, top, 100 + LINE_WIDTH, 100 + LINE_WIDTH),  LINE_WIDTH+3)
    pygame.display.update()

def kill_animation(frame):
    image = str(frame)
    if frame < 10:
        image = "0" + str(frame)
    display_image(screen, "Assets/animation2/sprite_" + image + ".jpeg", (800, 400), (150, 200))
    

def half_heal_animation(frame):
    image = str(frame)
    if frame < 10:
        image = "0" + str(frame)
    display_image(screen, "Assets/animation1/sprite_" + image + ".jpeg", (800, 400), (150, 200))    

def full_heal_animation(frame):
    image = str(frame)
    if frame < 10:
        image = "0" + str(frame)
    display_image(screen, "Assets/animation1/sprite_" + image + ".jpeg", (800, 400), (150, 200))    

def vaccine_animation(frame):
    image = str(frame)
    if frame < 10:
        image = "0" + str(frame)

def witch_infect(frame):
    image = str(frame)
    if frame < 10:
        image = "0" + str(frame)
    display_image(screen, "Assets/animation3/sprite_" + image + ".jpeg", (800, 500), (150, 200))

def direction(coord1, coord2):
    if coord2[0] > coord1[0]:
        return "moveUp"
    elif coord2[0] < coord1[0]:
        return "moveDown"
    elif coord2[1] > coord1[1]:
        return "moveRight"
    elif coord2[1] < coord1[1]:
        return "moveLeft"

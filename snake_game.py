
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define ROYGBIV colors
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
current_color_index = 0  # Start with red

# Initial variables
snake_speed = 10
speed_increment = 2  # How much the speed increases after eating food
game_speed = 150  # Start with a slower initial speed (in milliseconds)

def generate_food():
    global current_color_index
    size = random.choice([1, 2, 3])
    food_x = random.randint(0, (width // (snake_block_size * size)) - 1) * (snake_block_size * size)
    food_y = random.randint(0, (height // (snake_block_size * size)) - 1) * (snake_block_size * size)
    color = colors[current_color_index]
    current_color_index = (current_color_index + 1) % len(colors)  # Move to the next color
    print(f"Generated food of size {size} at position ({food_x}, {food_y}) with color {color}")
    return (food_x, food_y, size, color)

# Set up the display
width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define snake initial position and size
snake_block_size = 10
snake = [(100, 50), (90, 50), (80, 50)]  # Initial snake with 3 blocks
direction = "RIGHT"

food = generate_food()
score = 0

def draw_food(window, food):
    food_x, food_y, size, color = food
    pygame.draw.rect(window, color, pygame.Rect(food_x, food_y, snake_block_size * size, snake_block_size * size))

def draw_snake(window, snake):
    for i, block in enumerate(snake):
        color = colors[i % len(colors)]  # Cycle through the colors as the snake grows
        pygame.draw.rect(window, color, pygame.Rect(block[0], block[1], snake_block_size, snake_block_size))

def move_snake(snake, direction):
    x, y = snake[0]
    if direction == "UP":
        y -= snake_speed
    elif direction == "DOWN":
        y += snake_speed
    elif direction == "LEFT":
        x -= snake_speed
    elif direction == "RIGHT":
        x += snake_speed

    # Screen wrapping logic
    if x < 0:
        x = width - snake_block_size
    elif x >= width:
        x = 0
    if y < 0:
        y = height - snake_block_size
    elif y >= height:
        y = 0

    new_head = (x, y)
    snake.insert(0, new_head)
    snake.pop()

def show_score(window, score):
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

def game_over():
    font = pygame.font.SysFont(None, 50)
    game_over_text = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
    window.blit(game_over_text, (width // 6, height // 3))
    pygame.display.update()
    pygame.time.delay(2000)  # Wait for 2 seconds before closing the game
    pygame.quit()
    sys.exit()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    move_snake(snake, direction)

    if snake[0][0] in range(food[0], food[0] + snake_block_size * food[2]) and \
       snake[0][1] in range(food[1], food[1] + snake_block_size * food[2]):
        print(f"Snake ate food of size {food[2]}")
        for _ in range(food[2]):
            snake.append(snake[-1])
            colors.append(food[3])  # Add the color of the food to the snake's color list
        score += (4 - food[2]) * 10  # Smaller food gives more points
        print(f"Added {(4 - food[2]) * 10} points. Total score: {score}")
        
        # Gradually increase speed
        game_speed = max(10, game_speed - (speed_increment * food[2]))  # Decrease game_speed by 2 ms based on food size

        food = generate_food()  # Generate new food after eating

    if snake[0] in snake[1:]:
        game_over()

    window.fill((0, 0, 0))
    draw_snake(window, snake)
    draw_food(window, food)
    show_score(window, score)
    pygame.display.update()
    pygame.time.delay(game_speed)  # Use the dynamically adjusted game_speed

    

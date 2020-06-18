import pygame
import random
import src.Constants as cs
from src.Userinput import get_background


class Game():
    pygame.font.init()

    def __init__(self):
        self.window = pygame.display.set_mode((cs.window_lenght, cs.window_lenght))
        self.background = pygame.image.load(get_background())
        self.font1 = pygame.font.SysFont("Arial Black", 40, 0)
        self.font2 = pygame.font.SysFont("Arial", 12, 1)
        self.font3 = pygame.font.SysFont("Arial", 18, 1)
        self.font4 = pygame.font.SysFont("Calibri", 30, 1)
        self.credit = self.font2.render("Adam Lisichin", True, cs.white)
        self.text = self.font1.render(f'SNAKE GAME', True, cs.white)
        self.text2 = self.font3.render(f'Press any button to play / ESC to quit', True, cs.red)
        self.text4 = self.font4.render(f'Press SPACEBAR to resume', True, cs.blue)
        self.text5 = self.font2.render(f'Press ESC to quit', False, cs.red)
        self.clock = pygame.time.Clock()

    def display_on_screen(self, textinput, coordinates):
        return self.window.blit(textinput, coordinates)

    def get_scoreboard(self, score):
        score_text = self.font1.render(f'Score: {score}', True, cs.white)
        return score_text

    def get_final_score(self, score):
        final_score = self.font3.render(f'You lost. Score:{score} Press any button to play again', True, cs.red)
        return final_score

    def draw_grid(self):
        pygame.draw.rect(self.window, cs.map_color, pygame.Rect(cs.x_start, cs.x_start, cs.map_size, cs.map_size))
        for i in range(cs.block_size - 1):
            pygame.draw.line(self.window, cs.green, (cs.x_start, cs.x_next + cs.block_size * i), (cs.x_border, cs.x_next + cs.block_size * i))
            pygame.draw.line(self.window, cs.green, (cs.x_next + cs.block_size * i, cs.x_start), (cs.x_next + cs.block_size * i, cs.x_border))
        pygame.draw.polygon(self.window, cs.green, [(cs.x_start, cs.x_start), (cs.x_border, cs.x_start), (cs.x_border, cs.x_border), (cs.x_start, cs.x_border)], 1)

    def __str__(self):
        return f'Game'


class Wall():
    def __init__(self, position):
        self.position = position

    def get_wall_position(self):
        return self.position

    def draw_wall(self, game):
        for positions in self.get_wall_position():
            pygame.draw.rect(
                game.window, pygame.Color(
                    3, 0, 253), pygame.Rect(positions[0], positions[1], cs.block_size, cs.block_size))

    def positions_to_avoid(self, rate):
        avoid_these = []
        for coords in self.position:
            x = coords[0]
            y = coords[1]
            if x in range(cs.x_start, cs.x_border) and y in range(cs.x_start, cs.x_border):
                avoid_these.append([x + rate * cs.block_size, y + rate * cs.block_size])
                avoid_these.append([x, y + rate * cs.block_size])
                avoid_these.append([x - rate * cs.block_size, y + rate * cs.block_size])
                avoid_these.append([x + rate * cs.block_size, y])
                avoid_these.append([x, y])
                avoid_these.append([x - rate * cs.block_size, y])
                avoid_these.append([x + rate * cs.block_size, y - rate * cs.block_size])
                avoid_these.append([x, y - rate * cs.block_size])
                avoid_these.append([x - rate * cs.block_size, y - rate * cs.block_size])
        return avoid_these

    def __str__(self):
        return f'Wall'


class Snake():
    def __init__(self):
        self.position = [cs.snake_x, cs.snake_y]
        self.body = [self.position]
        self.direction = random.choice([cs.left, cs.right, cs.up, cs.down])

    def change_direction_to(self, direction):
        if direction == cs.right and self.direction != cs.left:
            self.direction = cs.right

        elif direction == cs.left and self.direction != cs.right:
            self.direction = cs.left

        elif direction == cs.up and self.direction != cs.down:
            self.direction = cs.up

        elif direction == cs.down and self.direction != cs.up:
            self.direction = cs.down

    def move(self, entity_position):
        if self.direction == cs.right:
            self.position[0] += cs.block_size
            if self.position[0] > cs.x_end:
                self.position[0] = cs.x_start

        elif self.direction == cs.left:
            self.position[0] -= cs.block_size
            if self.position[0] < cs.x_start:
                self.position[0] = cs.x_end

        elif self.direction == cs.up:
            self.position[1] -= cs.block_size
            if self.position[1] < cs.x_start:
                self.position[1] = cs.x_end

        elif self.direction == cs.down:
            self.position[1] += cs.block_size
            if self.position[1] > cs.x_end:
                self.position[1] = cs.x_start

        self.body.insert(0, list(self.position))
        if self.position == entity_position:
            return True
        else:
            self.body.pop()
            return False

    def collided_with_body(self):
        for body_part in self.body[1:]:
            if self.position == body_part:
                return True

        if self.direction == cs.left:
            if self.position == [self.body[-1][0] + cs.block_size, self.body[-1][1]]:
                return True

        elif self.direction == cs.right:
            if self.position == [self.body[-1][0] - cs.block_size, self.body[-1][1]]:
                return True

        elif self.direction == cs.up:
            if self.position == [self.body[-1][0], self.body[-1][1] + cs.block_size]:
                return True

        elif self.direction == cs.down:
            if self.position == [self.body[-1][0], self.body[-1][1] - cs.block_size]:
                return True
        return False

    def collided_with_wall(self, wall):
        for body_part in self.body:
            if body_part in wall.position:
                return True
        return False

    def get_body(self):
        return self.body

    def draw_snake(self, game):
        for positions in self.get_body():
            pygame.draw.rect(
                game.window, pygame.Color(
                    0, 225, 0), pygame.Rect(positions[0], positions[1], cs.block_size, cs.block_size))

    def __str__(self):
        return f'Snake'


class Food():
    def __init__(self):
        self.position = [
            random.randrange(
                cs.x_start, cs.x_end, cs.block_size), random.randrange(cs.x_start, cs.x_end, cs.block_size)
        ]
        self.is_food_on_screen = True

    def spawn_food(self):
        if not self.is_food_on_screen:
            self.position = [
                random.randrange(
                    cs.x_start, cs.x_end, cs.block_size), random.randrange(cs.x_start, cs.x_end, cs.block_size)
            ]
            self.is_food_on_screen = True
        return self.position

    def set_food(self, boolean):
        self.is_food_on_screen = boolean

    def draw_food(self, foodobject, game):
        drawn_food = pygame.draw.rect(
            game.window, pygame.Color(226, 30, 19), pygame.Rect(foodobject[0], foodobject[1], cs.block_size, cs.block_size)
        )
        return drawn_food

    def __str__(self):
        return f'Food'

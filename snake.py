import pygame
import sys
from pygame import mixer
from src.Game import Game, Snake, Food, Wall
from src.Userinput import get_tickrate, get_users_map, get_wall_cords_from_file, get_spawnrange
import src.Constants as cs


pygame.init()
mixer.init()
game = Game()
rate = get_spawnrange()


def game_over():
    print(f'Your score: {score}')
    pygame.quit()
    sys.exit()


def game_pause():  # pause menu
    paused = True
    while paused:
        pygame.draw.rect(game.window, cs.map_color, pygame.Rect(cs.x_start, cs.x_start, cs.map_size, cs.map_size))
        game.display_on_screen(game.text4, cs.text4_pos)
        pygame.display.update()
        mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                    mixer.music.unpause()
                elif event.key == pygame.K_ESCAPE:
                    game_over()


def game_intro():  # introduction menu
    intro = True
    while intro:
        game.window.fill(cs.black)
        game.display_on_screen(game.text, cs.text_pos)
        game.display_on_screen(game.text2, cs.text2_pos)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    game_loop()


def game_loop():
    global score
    score = 0
    snake = Snake()
    food = Food()
    wall = Wall(get_wall_cords_from_file(get_users_map()))
    game.get_scoreboard(score)  # get scoreboard based on current score
    pygame.display.set_caption(cs.title)  # display title on the bar
    mixer.music.load(cs.song_name)
    mixer.music.play(-1)  # loop the sound
    game_is_over = False
    while True:
        game.display_on_screen(game.background, cs.start_point)  # displays background from top left angle (0,0)
        game.display_on_screen(game.get_scoreboard(score), cs.scoreboard_pos)  # displays scoreboard at its coordinates
        game.display_on_screen(game.credit, cs.credit_pos)  # displays credit at its coordinates
        game.draw_grid()  # draws grid

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_direction_to(cs.right)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction_to(cs.left)
                elif event.key == pygame.K_UP:
                    snake.change_direction_to(cs.up)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction_to(cs.down)
                elif event.key == pygame.K_SPACE:
                    game_pause()
                elif event.key == pygame.K_ESCAPE:
                    game_over()

        while game_is_over:
            mixer.music.stop()
            game.window.fill(cs.black)
            game.display_on_screen(game.get_final_score(score), cs.text3_pos)
            game.display_on_screen(game.text5, cs.text5_pos)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over()
                    else:
                        game_loop()

        if food.spawn_food() not in snake.body[1:] and food.spawn_food() not in wall.positions_to_avoid(rate):
            food_pos = food.spawn_food()
            food.draw_food(food_pos, game)
        else:
            food.set_food(False)
            food_pos = []

        snake.draw_snake(game)
        wall.draw_wall(game)

        if snake.move(food_pos):
            score += 1
            game.get_scoreboard(score)
            food.set_food(False)

        pygame.display.flip()
        game.clock.tick(get_tickrate() + score * cs.increment)

        if snake.collided_with_body() or snake.collided_with_wall(wall):
            game.clock.tick(10)
            pygame.display.flip()
            pygame.time.delay(100)
            game_is_over = True


if __name__ == "__main__":
    game_intro()

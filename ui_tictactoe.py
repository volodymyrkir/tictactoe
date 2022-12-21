import sys
import pygame
from random import choice
from datetime import datetime
from ticitactoe import View
from log import get_logger

logger= get_logger()
pygame.init()
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("TIC TAC TOE")
rect_color = (255, 0, 0)


class PygameView(View):
    class Node:
        def __init__(self, x, y, width, height):
            self.rect = pygame.Rect(x, y, width, height)
            self.x = x
            self.y = y

    background = pygame.image.load('background.jpg').convert()

    locations = [(250, 120, 100, 100), (250 + 150, 120, 100, 100), (250 + 300, 120, 100, 100),
                 (250, 120 + 145, 100, 100), (250 + 150, 120 + 145, 100, 100), (250 + 300, 145 + 120, 100, 100),
                 (250, 120 + 290, 100, 100), (250 + 150, 120 + 290, 100, 100), (250 + 300, 290 + 120, 100, 100)]
    nodes = []
    moves = []
    turn = choice(["x", "o"])
    turn_stuff = {"x": pygame.image.load('x.jpg'), "o": pygame.image.load('o.jpg')}

    def init_loop(self):
        screen.blit(self.background, (0, 0))
        font = pygame.font.SysFont('ghotic', 60)
        welcome_label = font.render('WELCOME TO THE TIC TAC TOE GAME!', True, pygame.Color(220, 20, 60))
        welcome_rect = welcome_label.get_rect()
        welcome_rect.center = (900 // 2, 100)

        new_game_label = font.render('New game', True, pygame.Color(220, 20, 60))
        new_game_rect = new_game_label.get_rect()
        new_game_rect.center = (900 // 2, 250)

        show_log_label = font.render('Show win log file', True, pygame.Color(220, 20, 60))
        show_log_rect = show_log_label.get_rect()
        show_log_rect.center = (900 // 2, 350)

        clear_log_label = font.render('Clear win log file', True, pygame.Color(220, 20, 60))
        clear_log_rect = clear_log_label.get_rect()
        clear_log_rect.center = (900 // 2, 450)

        exit_label = font.render('Exit', True, pygame.Color(220, 20, 60))
        exit_rect = exit_label.get_rect()
        exit_rect.center = (900 // 2, 600)
        screen.blit(welcome_label, welcome_rect)
        screen.blit(new_game_label, new_game_rect)
        screen.blit(show_log_label, show_log_rect)
        screen.blit(clear_log_label, clear_log_rect)
        screen.blit(exit_label, exit_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if new_game_rect.collidepoint(pygame.mouse.get_pos()):
                        self.show_board()
                    elif show_log_rect.collidepoint(pygame.mouse.get_pos()):
                        logs = ""
                        with open("wins.log", "r", encoding="utf-8") as file:
                            for line in file:
                                logs += line #TODO
                        print(logs)
                    elif clear_log_rect.collidepoint(pygame.mouse.get_pos()):
                        open("wins.log", "w", encoding="utf-8").close()
                        logger.warning("Log file cleared")
                    elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                        sys.exit()
            pygame.display.update()

    def rect_collided(self, point):
        for node in self.nodes:
            if node.rect.collidepoint(point):
                return self.nodes.index(node), node.x, node.y
        return None, None, None

    def show_board(self):
        font = pygame.font.SysFont('ghotic', 50)
        for position in self.locations:
            n = self.Node(*position)
            self.nodes.append(n)
        turn_label = font.render(f"{self.turn}`s turn now!", True, pygame.Color(220, 20, 60))
        while True:
            screen.blit(self.background, (0, 0))
            screen.blit(turn_label, (350, 35))
            for node in self.nodes:
                pygame.draw.rect(screen, rect_color, node.rect, 2)

            for move in self.moves:
                picture = pygame.transform.scale(move[0], (100, 100))
                screen.blit(picture, (move[1], move[2]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    node_index, collided_x, collided_y = self.rect_collided(pygame.mouse.get_pos())
                    if node_index is not None and self.field.field[node_index] == " ":
                        self.field.field[node_index] = self.turn
                        self.moves.append((self.turn_stuff[self.turn], collided_x, collided_y))
                        if self.field.check_all(self.turn, 9):
                            logger.info(f"{self.turn} Wins!!! {datetime.now()}")
                            exit_label = font.render(f"{self.turn} won, click this message to go to main menu!",
                                                     True, pygame.Color(220, 20, 60))
                            exit_rect = exit_label.get_rect()
                            exit_rect.center = (500, 600)
                            screen.blit(exit_label, exit_rect)
                            while True:
                                pygame.display.update()
                                for move in self.moves:
                                    picture = pygame.transform.scale(move[0], (100, 100))
                                    screen.blit(picture, (move[1], move[2]))
                                for ev in pygame.event.get():
                                    if ev.type == pygame.MOUSEBUTTONDOWN:
                                        if exit_rect.collidepoint(pygame.mouse.get_pos()):
                                            self.field.field=[" " for _ in range(9)]
                                            self.change_turn()
                                            self.moves=[]
                                            self.nodes=[]
                                            self.init_loop()
                        elif self.field.draw_check():
                            logger.info(f"Draw.{datetime.now()}")
                            exit_label = font.render(f"Draw! Click this message to go to main menu!",
                                                     True, pygame.Color(220, 20, 60))
                            exit_rect = exit_label.get_rect()
                            exit_rect.center = (500, 600)
                            screen.blit(exit_label, exit_rect)
                            while True:
                                pygame.display.update()
                                for move in self.moves:
                                    picture = pygame.transform.scale(move[0], (100, 100))
                                    screen.blit(picture, (move[1], move[2]))
                                for ev in pygame.event.get():
                                    if ev.type == pygame.MOUSEBUTTONDOWN:
                                        if exit_rect.collidepoint(pygame.mouse.get_pos()):
                                            self.field.field = [" " for _ in range(9)]
                                            self.change_turn()
                                            self.moves = []
                                            self.nodes = []
                                            self.init_loop()
                        self.change_turn()
                        turn_label = font.render(f"{self.turn}`s turn now!", True, pygame.Color(220, 20, 60))
            pygame.display.update()

    def change_turn(self):
        if self.turn == "x":
            self.turn = "o"
        else:
            self.turn = "x"

    def print_instructions(self, name1, name2):
        pass

    def get_game_choice(self):
        pass

    def get_menu_choice(self):
        pass

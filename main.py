import pygame

import sys

import random

from pygame import MOUSEBUTTONDOWN, QUIT, mixer



pygame.init()

pygame.font.init()



# fonts

main_font = pygame.font.SysFont("comicsand", 44)

main_font_small = pygame.font.SysFont("comicsand", 30)



# images

LADDER = pygame.transform.scale(pygame.image.load("images/ladder.png"), (160, 270))



# predefining colors

BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

GREEN = (0, 255, 0)

RED = (255, 0, 0)

BLUE = (0, 0, 255)

YELLOW = (200, 150, 18)

PINK = (255, 79, 88)

WHITE_SMOKE = (240, 246, 247)

DEEP = (102, 157, 179)

SMOOTH = (28, 28, 28)



TILE_SIZE = 80

COLS = 10

ROWS = 10



# piece radius

PIECE = 20



# display settings

WIDTH, HEIGHT = 1000, 800



WIN = pygame.display.set_mode((WIDTH, HEIGHT))



pygame.display.set_caption("Snakes and Ladders")



# ladder lists

init_ladders = [[4, 14], [17, 36], [41, 52], [55, 77], [83, 93]]



# questions to answer after moving

questions = {

    "What is the capital of Australia?": ["Canberra", "Sydney", "Melbourne"],

    "On what continent is 'Bhutan' located?": ["Asia", "Afrika", "South Amerika"],

    "Where do penguins live?": ["Antarktika", "North Pole", "Both"]

}



question_answers = {

    "What is the capital of Australia?": "Canberra",

    "On what continent is 'Bhutan' located?": "Asia",

    "Where do penguins live?": "Antarktika"

}



# main board class with game handling

class Board:

    def __init__(self, p1, p2):

        self.x = 0

        self.y = HEIGHT

        self.color_choice = [WHITE_SMOKE, PINK, DEEP]

        self.colors = [random.choice(self.color_choice) for _i in range(ROWS) for _j in range(COLS)]

        self.coor = []



        self.p1 = p1

        self.p2 = p2

        self.turn = self.p1

        self.turn_color = PINK

  

    def draw(self): # drawing the board onto the screen

        number = 1

        y_pos = 1

        for i in range(ROWS):

            x_pos = self.x

            for i in range(COLS):

                r = pygame.Rect(x_pos * TILE_SIZE, HEIGHT - y_pos * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                pygame.draw.rect(WIN, self.colors[number - 1], r)

                pygame.draw.rect(WIN, SMOOTH, r, 3)

                WIN.blit(main_font.render(str(number), 1, BLACK), (x_pos * TILE_SIZE + 10, HEIGHT - y_pos * TILE_SIZE + 10))

                

                x_pos += 1

                number += 1



            y_pos += 1



    def winner(self, player): # checking for winner

        if player.won:

            return True

        return False



    def change_turn(self, turn): # changing game turn

        if self.turn == self.p1:

            self.turn = self.p2

            self.turn_color = DEEP

        else:

            self.turn = self.p1

            self.turn_color = PINK



        turn.update(self.turn_color, self.turn.name + "'s Turn")



        self.turn.finished = False



    def check_same_coor(self, p1, p2): # check if both pieces are at the same coordinates

        if p1.x == p2.x and p1.y == p2.y:

            return True

        return False



    def choose_question(self, answers, used_questions): # choose a random question

        global questions

        if len(list(questions)) == len(used_questions):

            used_questions = []

        question = random.choice(list(questions))

        counter = 0 # to avoid lags

        while question in used_questions:

            question = random.choice(list(questions))

            counter += 1

            if counter >= 10:

                for k in questions.keys():

                    if k not in used_questions:

                        question = k

                        break



        used_questions.append(question)

        random.shuffle(questions[question])

        for i in range(3):

            q = main_font.render(questions[question][i], 1, WHITE)

            x = 150 + (i * 350) - q.get_width() / 2

            y = random.randrange(-600, -350)



            answer = Button(x, y, q.get_width(), q.get_height(), (23, 81, 126), questions[question][i], BLACK)

            answers.append(answer)



        correct_answer = question_answers[question]



        question = main_font.render(question, 1, BLACK)



        return (correct_answer, question, used_questions)



# ladder class

class Ladder:

    def __init__(self, start: int, end: int):

        self.img = LADDER

        self.x = 0

        self.y = 0

        self.height = 0

        self.width = TILE_SIZE * 2



        self.start = start

        self.end = end



        self.create()



    def create(self): # creating the ladder at proper coordinates with proper size in the beginning

        if self.end < self.start:

            start = str(self.end - 1)

            end = str(self.start - 1)

        else:

            start = str(self.start - 1)

            end = str(self.end - 1)

        if len(start) == 1:

            y_pos = 0

            x_pos = int(start)

        else:

            y_pos = int(start[0])

            x_pos = int(start[1])



        x_pos_end = int(end[1])

        y_pos_end = int(end[0]) + 1



        self.x = x_pos_end * TILE_SIZE

        self.y = HEIGHT - y_pos_end * TILE_SIZE + 20



        self.height =  abs(self.y - (HEIGHT - y_pos * TILE_SIZE))



        self.img = pygame.transform.scale(self.img, (self.width, self.height))



        if len(str(self.start)) > 1:

            if int(str(self.start)[1]) > int(str(self.end)[1]):

                self.img = pygame.transform.flip(self.img, True, False)

            else:

                self.end += 1



        else:

            if self.start <= int(str(self.end)[1]):

                self.end += 1

        print(self.end)





    def draw(self): # drawing the ladder onto the screen

        WIN.blit(self.img, (self.x, self.y))



        



# player piece

class Piece:

    def __init__(self, x, y, color, name: str):

        self.x = x

        self.y = y

        self.number = 1

        self.color = color

        self.won = False

        self.name = name

        self.move_time = 0

        self.r = 25



        self.finished = False

        self.end_num = 1



    def draw(self): # drawing the piece onto the screen

        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.r)



    def change_num(self, num): # change piece number / pos

        self.end_num = self.number + num



    def move_animation(self, ladders): # move the piece with animation

        self.move_time += 1



        if self.number == 100:

            self.won = True



        if self.move_time % 20 == 0:

            if self.number % 10 == 0:

                self.y -= TILE_SIZE

                self.x = TILE_SIZE / 2

            else:

                self.x += TILE_SIZE

            

            self.number += 1



        if self.number >= self.end_num:

            for ladder in ladders:

                if self.end_num == ladder.start:

                    while self.number < ladder.end:

                        if self.number % 10 == 0:

                            self.y -= TILE_SIZE

                            self.x = TILE_SIZE / 2

                        else:

                            self.x += TILE_SIZE



                        self.number += 1



                    self.number = ladder.end

                    self.end_num = self.number

                    break



                elif self.end_num == ladder.end:

                    while self.number != ladder.start:

                        if self.number % 10 == 0:

                            self.y += TILE_SIZE

                            self.x = TILE_SIZE / 2

                            self.number -= 19

                        else:

                            self.x += TILE_SIZE



                            self.number += 1



                    self.number = ladder.start

                    self.end_num = self.number

                    break



            self.move_time = 0

            self.finished = True

            self.number = self.end_num

            return False



    def reset(self): # resetting the piece size

        self.r = 25



    def check_r(self): # check if the radius equals initial radius

        if self.r != 25:

            return True

        return False



# dice class 

class Dice:

    def __init__(self, x, y) -> None:

        self.x = x

        self.y = y

        self.width = 200

        self.height = 200

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.value = 5

        self.color = (100, 100, 100)



    def draw(self): # drawing dice number

        text = main_font.render(str(self.value), 1, BLACK)

        

        pygame.draw.rect(WIN, self.color, self.rect)

        WIN.blit(text, (self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))



    def roll(self): # rolling the dice

        self.value = random.randint(1, 6)

        return self.value 



# button class

class Button:

    def __init__(self, x, y, width, height, color, text, outline=None, r=None):

        self.x = x

        self.y = y

        self.width = width

        self.height = height

        self.color = color

        self.text = text

        self.font = main_font

        self.text_surf = main_font.render(self.text, 1, (0, 0, 0))

        self.outline = outline

        self.r = r



        self.rect = pygame.Rect(x, y, width, height)

        self.outline_width = 3



    def draw(self, surface): # drawing button

        if self.r:

            pygame.draw.rect(surface, self.color, self.rect, 0, self.r)

            if self.outline:

                pygame.draw.rect(surface, self.outline, self.rect, self.outline_width, self.r)

        else:

            pygame.draw.rect(surface, self.color, self.rect)

            if self.outline:

                pygame.draw.rect(surface, self.outline, self.rect, self.outline_width)

        

        surface.blit(self.text_surf, (self.x + self.width / 2 - self.text_surf.get_width() / 2, self.y + self.height / 2 - self.text_surf.get_height() / 2))



    def click(self): # check for mouse click

        m = pygame.mouse.get_pos()

        if self.rect.collidepoint(m):

            return True



        return False



    def change_font(self, font): # changing button text font

        self.font = font

        self.text_surf = self.font.render(self.text, 1, (0, 0, 0))



    def update(self, color, text): # updating the button values

        self.color = color

        self.text_surf = self.font.render(text, 1, (0, 0, 0))



# main function

def main():

    clock = pygame.time.Clock()

    FPS = 60

    run = True



    active = False



    player1 = Piece(TILE_SIZE / 2, HEIGHT - TILE_SIZE / 2, SMOOTH, "Player 1")

    player2 = Piece(TILE_SIZE / 2, HEIGHT - TILE_SIZE / 2, (60, 60, 255), "Player 2")



    board = Board(player1, player2)



    roll = Button(WIDTH- 200, HEIGHT - 203, 200, 200, (150, 150, 150), "roll", WHITE_SMOKE)

    turn = Button(WIDTH - 200, 0, 200, 30, board.turn_color, board.turn.name + "'s Turn")



    turn.change_font(main_font_small)



    dice = Dice(WIDTH - 200, HEIGHT - 550)



    ladders = []



    for l in init_ladders: # creating the ladders

        ladder = Ladder(l[0], l[1])

        ladders.append(ladder)



    move_time = 0



    def redraw_window(): # redrawing window with every frame (every element)

        WIN.fill(SMOOTH)



        board.draw()



        for ladder in ladders:

            ladder.draw()



        dice.draw()



        player2.draw()

        player1.draw()

        



        roll.draw(WIN)



        turn.draw(WIN)



        pygame.display.update()



    while run: # mainloop

        clock.tick(FPS)



        # check for winner

        if board.winner(player1):

            return restart_menu(player1)

        elif board.winner(player2):

            return restart_menu(player2)



        # check for events

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                sys.exit()

            

            if event.type == MOUSEBUTTONDOWN:

                if roll.click():

                    if board.turn.number == board.turn.end_num:

                        active = False

                        number = dice.roll()

                        board.turn.change_num(number)

                        board.turn.finished = False



        # checking if both pieces have same coordinates

        if board.check_same_coor(player1, player2):

            board.turn.r *= 0.6



        # redrawing window every frame

        redraw_window()



        # resetting the piece size

        if board.turn.check_r():

            board.turn.reset()



        # counter

        if board.turn.end_num > board.turn.number:

            board.turn.move_animation(ladders)

        if board.turn.finished:

            board.change_turn(turn)





# restart menu after game is over

def restart_menu(player):

    clock = pygame.time.Clock()

    run = True

    FPS = 60



    name = player.name



    def redraw_window():





        pygame.display.update()

    

    while run:

        clock.tick(FPS)



        for event in pygame.event.get():

            if event.type == QUIT:

                quit()



        redraw_window()







main()
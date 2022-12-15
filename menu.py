import pygame
import sys
from highscore import read_highscores


class UserInterface:
    def __init__(self):
        # Init pygame and mixer
        pygame.init()
        pygame.mixer.init()
        self.menu = True

        # set constants for the menu
        self.size = self.width, self.height = 1920, 1080
        self.white, self.purple, self.gold, self.silver, self.bronze = "#ffffff", \
                                                                       '#810CA8', '#FFBF00', '#B2B2B2', '#C58940'
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.screen = pygame.display.set_mode(self.size)
        self.screen_center = self.screen.get_rect().center
        self.show_high_score = False
        self.fps = 60

        # load menu sound
        self.menu_sound = pygame.mixer.Sound("res/sound/menu_sound.mp3")

        # load background image
        self.bg_image = pygame.image.load('res/img/bg_image.png')

        # initialize title and title center for align center
        self.title = pygame.image.load('res/img/title.png')
        self.title_rect = self.title.get_rect()
        self.title_rect.center = self.screen_center

        # initialize subtitle text and center for align center
        self.subtitle = self.font.render('Who wants to be a millionaire?', True, self.white)
        self.subtitle_text_rect = self.subtitle.get_rect()
        self.subtitle_text_rect.center = self.screen_center

        # initialize welcome text and center for align center
        self.welcome_text = self.font.render('Welcome to', True, self.white)
        self.welcome_text_rect = self.welcome_text.get_rect()
        self.welcome_text_rect.center = self.screen_center

        # set play and exit buttons
        self.play = pygame.image.load('res/img/play.png')
        self.play_hover = pygame.image.load('res/img/play2.png')
        self.play_rect = self.play.get_rect()
        self.play_rect.center = self.screen_center
        self.exit_game = pygame.image.load('res/img/exit.png')
        self.exit_game_hover = pygame.image.load('res/img/exit_2.png')
        self.exit_game_rect = self.exit_game.get_rect()
        self.exit_game_rect.center = self.screen_center
        self.high_score = pygame.image.load('res/img/highscores.png')
        self.high_score_hover = pygame.image.load('res/img/highscores_hover.png')
        self.high_score_rect = self.exit_game.get_rect()
        self.high_score_rect.center = self.screen_center
        self.back = pygame.image.load('res/img/back.png')
        self.back_hover = pygame.image.load('res/img/back_hover.png')
        self.back_rect = self.exit_game.get_rect()
        self.back_rect.center = self.screen_center


class Menu(UserInterface):

    def show_high_score_function(self, mx, my, event):

        if 1289 > mx > self.play_rect.x and 840 > my > 800:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.show_high_score = False
        self.screen.blit(self.bg_image, (0, 0))
        if 1289 > mx > self.play_rect.x and 840 > my > 800:
            back_style = self.back_hover
        else:
            back_style = self.back
        self.screen.blit(back_style, (self.exit_game_rect.x, 800))
        highscores = read_highscores()
        y_coord = 0
        nickname = self.font.render("Nickname", True, self.white)
        amount = self.font.render("Amount", True, self.white)
        date = self.font.render("Date", True, self.white)
        self.screen.blit(nickname, (540, 250))
        self.screen.blit(amount, (900, 250))
        self.screen.blit(date, (1220, 250))
        for i in range(len(highscores)):
            if y_coord == 0:
                color = self.gold
            elif y_coord == 60:
                color = self.silver
            elif y_coord == 120:
                color = self.bronze
            else:
                color = self.purple
            pygame.draw.rect(self.screen, color, pygame.Rect(460, 300 + y_coord, 40, 48))
            pygame.draw.rect(self.screen, self.purple, pygame.Rect(510, 300 + y_coord, 350, 48), 2)
            pygame.draw.rect(self.screen, self.purple, pygame.Rect(870, 300 + y_coord, 300, 48), 2)
            pygame.draw.rect(self.screen, self.purple, pygame.Rect(1180, 300 + y_coord, 250, 48), 2)
            score = self.font.render(f'{i + 1}', True, self.white)
            name = self.font.render(f'{highscores[i]["name"]}', True, self.white)
            val = self.font.render(f'$ {format(highscores[i]["val"], ",")}', True, self.white)
            date = self.font.render(f'{highscores[i]["date"]}', True, self.white)
            self.screen.blit(score, (470, 310 + y_coord))
            self.screen.blit(name, (540, 310 + y_coord))
            self.screen.blit(val, (910, 310 + y_coord))
            self.screen.blit(date, (1220, 310 + y_coord))
            y_coord += 60

    def __init__(self):
        super().__init__()

        # menu function
        def game_menu():
            # start the menu sound and looping
            self.menu_sound.play(-1)
            while self.menu:
                # set variables for mouse coordinates
                mx, my = pygame.mouse.get_pos()
                # manage quit game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    # manage play button
                    if 1289 > mx > self.play_rect.x and 740 > my > 700:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.menu = False
                            self.menu_sound.stop()
                            pygame.time.wait(1000)
                    # manage exit button
                    if 1289 > mx > self.play_rect.x and 790 > my > 750:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.show_high_score = True
                    if 1289 > mx > self.play_rect.x and 840 > my > 800:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if not self.show_high_score:
                                sys.exit()
                    if self.show_high_score:
                        self.show_high_score_function(mx, my, event)
                # show background image
                if not self.show_high_score:
                    self.screen.blit(self.bg_image, (0, 0))
                # manage play button hover
                if 1289 > mx > self.play_rect.x and 740 > my > 700:
                    start_game = self.play_hover
                else:
                    start_game = self.play
                # manage highscore and exit button hover
                if 1289 > mx > self.play_rect.x and 790 > my > 750:
                    high_score_style = self.high_score_hover
                else:
                    high_score_style = self.high_score
                if 1289 > mx > self.play_rect.x and 840 > my > 800:
                    exit_game_style = self.exit_game_hover
                else:
                    exit_game_style = self.exit_game
                # show title, subtitle, welcome text, play and exit buttons
                if not self.show_high_score:
                    self.screen.blit(self.title, (self.title_rect.x, 190))
                    self.screen.blit(self.subtitle, (self.subtitle_text_rect.x, 600))
                    self.screen.blit(self.welcome_text, (self.welcome_text_rect.x, 550))
                    self.screen.blit(start_game, (self.play_rect.x, 700))
                    self.screen.blit(high_score_style, (self.high_score_rect.x, 750))
                    self.screen.blit(exit_game_style, (self.exit_game_rect.x, 800))
                # refresh the page
                pygame.display.flip()
                pygame.time.Clock().tick(self.fps)

        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            game_menu()
            pygame.display.update()

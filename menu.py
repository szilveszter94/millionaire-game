import pygame
import sys


class UserInterface:
    def __init__(self):
        # Init pygame and mixer
        pygame.init()
        pygame.mixer.init()
        self.menu = True

        # set constants for the menu
        self.size = self.width, self.height = 1920, 1080
        self.white = "#ffffff"
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.screen = pygame.display.set_mode(self.size)
        self.screen_center = self.screen.get_rect().center

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


class Menu(UserInterface):
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
                            sys.exit()
                # show background image
                self.screen.blit(self.bg_image, (0, 0))
                # manage play button hover
                if 1289 > mx > self.play_rect.x and 740 > my > 700:
                    start_game = self.play_hover
                else:
                    start_game = self.play
                # manage exit button hover
                if 1289 > mx > self.play_rect.x and 790 > my > 750:
                    exit_game_style = self.exit_game_hover
                else:
                    exit_game_style = self.exit_game
                # show title, subtitle, welcome text, play and exit buttons
                self.screen.blit(self.title, (self.title_rect.x, 190))
                self.screen.blit(self.subtitle, (self.subtitle_text_rect.x, 600))
                self.screen.blit(self.welcome_text, (self.welcome_text_rect.x, 550))
                self.screen.blit(start_game, (self.play_rect.x, 700))
                self.screen.blit(exit_game_style, (self.exit_game_rect.x, 750))
                # refresh the page
                pygame.display.flip()

        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            game_menu()
            pygame.display.update()

import pygame, sys
from question_bank import generate_questions
from audience_graph_generator import create_random_list
from highscore import write_highscore


def check_answers(res):
    if res:
        ans_bg = pygame.image.load('res/img/answers_correct.png')
    else:
        ans_bg = pygame.image.load('res/img/answers_incorrect.png')
    return ans_bg


class GameUI:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.nickname = "Anonymous"
        self.game = True
        self.ask_name = True
        self.fps = 60
        self.correct_sound = pygame.mixer.Sound('res/sound/correct_sound.mp3')
        self.wrong_sound = pygame.mixer.Sound('res/sound/wrong_sound.mp3')
        self.gold, self.purple, self.white = '#FFBF00', '#810CA8', '#ffffff'
        self.question_map = [True, True, True, True]
        self.questions = generate_questions()
        self.question_nr = 0
        self.answer_bg_xcoord = 360
        self.answer_bg_ycoord = 740
        self.question = self.questions[self.question_nr]['question']
        self.answers = self.questions[self.question_nr]['answers']
        self.correct = self.questions[self.question_nr]['correct']
        self.size = self.width, self.height = 1920, 1080
        self.prizes = ["100", "200", "300", "500", "1,000", "2,000", "4,000", "8,000",
                       "16,000", "32,000", "64,000", "125,000", "250,000", "500,000", "1,000,000"]
        self.y_coord = [i for i in range(498, 123, -25)]
        self.graph = self.clicked = self.half_cut = self.phone = self.audience = self.show_phone_result = False
        self.bg_image = pygame.image.load('res/img/bg_image.png')
        self.screen = pygame.display.set_mode(self.size)
        self.screen_center = self.screen.get_rect().center
        self.game_sound = pygame.mixer.Sound('res/sound/game_sound.mp3')
        self.half_cut_sound = pygame.mixer.Sound('res/sound/half_cut.mp3')
        self.audience_sound = pygame.mixer.Sound('res/sound/ask_the_audience.mp3')
        self.phone_sound = pygame.mixer.Sound('res/sound/phone_sound.mp3')
        self.random_arr = []
        self.score_bg = pygame.image.load('res/img/score_bg.png')
        self.stand = pygame.image.load('res/img/stand.png')
        self.stand_rect = self.stand.get_rect()
        self.fonts = [pygame.font.Font('freesansbold.ttf', i) for i in range(16, 29, 4)]
        self.help_tools = pygame.image.load('res/img/help_tools.png')
        self.remove_help = pygame.image.load('res/img/remove_help.png')
        self.answers_bg_1 = self.answers_bg_2 = self.answers_bg_3 = self.answers_bg_4 = pygame.image.load('res/img'
                                                                                                          '/answers.png')


class Game(GameUI):
    def __init__(self):
        super().__init__()

        def ask_the_nickname():
            user_text = ''
            input_rect = pygame.Rect(830, 600, 250, 32)
            color_active = '#C147E9'

            # color_passive store color(chartreuse4) which is
            # color of input box.
            color_passive = '#810CA8'
            color = color_passive

            active = False
            while self.ask_name:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_rect.collidepoint(event.pos):
                            active = True
                        else:
                            active = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if len(user_text) > 0:
                                self.nickname = user_text[0:14]
                                self.ask_name = False
                        # Check for backspace
                        if event.key == pygame.K_BACKSPACE:

                            # get text input from 0 to -1 i.e. end.
                            user_text = user_text[:-1]

                        # Unicode standard is used for string
                        # formation
                        else:
                            user_text += event.unicode
                    self.screen.blit(self.bg_image, (0, 0))

                    if active:
                        color = color_active
                    else:
                        color = color_passive

                    # draw rectangle and argument passed which should
                    # be on screen
                    pygame.draw.rect(self.screen, color, input_rect)
                    write_your_name = self.fonts[3].render("Write your nickname and press enter: ", True, self.white)
                    write_your_name_rect = write_your_name.get_rect()
                    write_your_name_rect.center = self.screen_center
                    text_surface = self.fonts[3].render(user_text, True, self.white)

                    # render at position stated in arguments
                    self.screen.blit(write_your_name, (write_your_name_rect.x, 550))
                    self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

                    # set width of textfield so that text cannot get
                    # outside of user's text input
                    input_rect.w = max(250, text_surface.get_width() + 10)

                    # display.flip() will update only a portion of the
                    # screen to updated, not full area
                    pygame.display.flip()

        def manage_help_tools_click(mx, my):
            if self.clicked:
                if 361 > mx > 212 and 143 < my < 237 and not self.half_cut:
                    self.half_cut = True
                    self.half_cut_sound.play()
                    half_cut_function()
                if 524 > mx > 375 and 143 < my < 237 and not self.phone:
                    self.phone = True
                    phone_function()
                if 686 > mx > 536 and 143 < my < 237 and not self.audience:
                    self.audience = True
                    audience_function()
                if 1362 > mx > 1211 and 143 < my < 237 and self.question_nr > 0:
                    game_over(self.prizes[self.question_nr - 1])

        def phone_function():
            self.game_sound.stop()
            self.phone_sound.play()
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            pygame.time.delay(5000)
            self.phone_sound.stop()
            pygame.event.clear()
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            self.game_sound.play(-1)
            self.show_phone_result = True

        def render_phone_result():
            if self.answers.index(self.correct) == 0:
                self.answers_bg_1 = pygame.image.load('res/img/answers_hover.png')
            if self.answers.index(self.correct) == 1:
                self.answers_bg_2 = pygame.image.load('res/img/answers_hover.png')
            if self.answers.index(self.correct) == 2:
                self.answers_bg_3 = pygame.image.load('res/img/answers_hover.png')
            if self.answers.index(self.correct) == 3:
                self.answers_bg_4 = pygame.image.load('res/img/answers_hover.png')

        def draw_audience_result():
            ans_letter = [self.fonts[2].render(f"{chr(i)}", True, self.gold) for i in range(ord("A"), ord("E"))]
            x_coor = 0
            for i in range(4):
                self.screen.blit(ans_letter[i], (353 + x_coor, 410))
                pygame.draw.rect(self.screen, [20, 50 + 2 * self.random_arr[i], 50],
                                 pygame.Rect(340 + x_coor, 400 - self.random_arr[i], 40, self.random_arr[i]))
                pygame.draw.rect(self.screen, self.purple, pygame.Rect(340 + x_coor, 300, 40, 100), 1)
                x_coor += 60

        def game_over(final_score):
            self.screen.blit(self.bg_image, (0, 0))
            if self.question_nr >= 9:
                render_score = self.fonts[3].render(f'Congratulations! Your final score is: $ {final_score}', True,
                                                    self.gold)
                render_score_rect = render_score.get_rect()
                render_score_rect.center = self.screen_center
            else:
                render_score = self.fonts[3].render(f'Unfortunately your final score is: $ {final_score}', True,
                                                    self.gold)
                render_score_rect = render_score.get_rect()
                render_score_rect.center = self.screen_center
            self.screen.blit(render_score, (render_score_rect.x, render_score_rect.y))
            pygame.display.flip()
            write_highscore([self.nickname, int(final_score.replace(',', ''))])
            pygame.time.delay(3000)
            self.game_sound.stop()
            self.game = False

        def audience_function():
            self.random_arr = create_random_list(self.answers, self.correct)
            self.graph = True
            self.game_sound.stop()
            self.audience_sound.play()
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            pygame.time.delay(5000)
            pygame.event.clear()
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            self.audience_sound.stop()
            self.game_sound.play(-1)

        def half_cut_function():
            two_bad = self.questions[self.question_nr]['two_bad']
            for i in range(len(self.answers)):
                if self.answers[i] in two_bad:
                    self.answers[i] = ""
                    self.question_map[i] = False

        def show_correct_or_false(res):
            self.graph = self.show_phone_result = False
            render_answers_background()
            render_answers()
            pygame.display.flip()
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            if res:
                self.correct_sound.play(1)
                pygame.time.delay(2000)
                self.correct_sound.stop()
            else:
                self.wrong_sound.play(1)
                pygame.time.delay(2000)
                self.wrong_sound.stop()
                final_score = '0'
                if self.question_nr == 14:
                    final_score = self.prizes[14]
                elif self.question_nr >= 9:
                    final_score = self.prizes[9]
                elif self.question_nr >= 5:
                    final_score = self.prizes[4]
                game_over(final_score)

            pygame.event.clear()
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            update_questions()

        def manage_question_length():
            words = [word.split(' ') for word in self.question.splitlines()]
            all_word = words[0]
            length = len(all_word) // 2
            first = all_word[0:length]
            second = all_word[length:len(all_word)]
            return [" ".join(first), " ".join(second)]

        def check_answers_length(ans):
            if len(ans) > 60:
                return self.fonts[0].render(ans, True, self.white)
            elif len(ans) > 40:
                return self.fonts[1].render(ans, True, self.white)
            else:
                return self.fonts[2].render(ans, True, self.white)

        def update_questions():
            if self.question_nr >= 14:
                game_over(self.prizes[14])
            self.question_nr += 1
            self.question = self.questions[self.question_nr]['question']
            self.answers = self.questions[self.question_nr]['answers']
            self.correct = self.questions[self.question_nr]['correct']
            self.question_map = [True, True, True, True]

        def render_prizes():
            self.screen.blit(self.score_bg, (1390, self.y_coord[self.question_nr]))
            prize_surfaces = []
            for i in range(len(self.prizes)):
                if (i + 1) % 5 == 0:
                    color = self.white
                else:
                    color = self.gold
                item = self.fonts[2].render(f'{i + 1}: $ {self.prizes[i]}', True, color)
                prize_surfaces.append(item)
            step = 0
            for i in range(len(prize_surfaces)):
                self.screen.blit(prize_surfaces[i], (1400, 500 - step))
                step += 25

        def render_background():
            question_bg = pygame.image.load('res/img/question.png')
            question_bg_rect = question_bg.get_rect()
            question_bg_rect.center = self.screen_center
            self.screen.blit(self.bg_image, (0, 0))
            self.screen.blit(question_bg, (question_bg_rect.x, 580))
            self.screen.blit(self.help_tools, (210, 140))
            if self.question_nr > 0:
                self.screen.blit(self.stand, (1210, 140))
            if self.half_cut:
                self.screen.blit(self.remove_help, (222, 152))
            if self.phone:
                self.screen.blit(self.remove_help, (382, 152))
            if self.audience:
                self.screen.blit(self.remove_help, (542, 152))
            if self.graph:
                draw_audience_result()
            render_prizes()

        def render_question():
            if len(self.question) > 86:
                splitted_question = manage_question_length()
                question_texts = [self.fonts[3].render(splitted_question[i], True, self.white) for i in range(2)]
                question_texts_rect = [question_texts[i].get_rect() for i in range(2)]
                for i in range(2):
                    question_texts_rect[i].center = self.screen_center
                self.screen.blit(question_texts[0], (question_texts_rect[0].x, 605))
                self.screen.blit(question_texts[1], (question_texts_rect[1].x, 640))
            else:
                question_text = self.fonts[3].render(self.question, True, self.white)
                question_text_rect = question_text.get_rect()
                question_text_rect.center = self.screen_center
                self.screen.blit(question_text, (question_text_rect.x, 620))

        def render_answers_background():
            ans_letter = [self.fonts[3].render(f"{chr(i)}:", True, self.gold) for i in range(ord("A"), ord("E"))]
            answers_bg_rect = self.answers_bg_1.get_rect()
            answers_bg_rect.center = self.screen_center
            if self.show_phone_result:
                render_phone_result()
            self.screen.blit(self.answers_bg_1, (answers_bg_rect.x - self.answer_bg_xcoord,
                                                 self.answer_bg_ycoord))
            self.screen.blit(self.answers_bg_2, (answers_bg_rect.x + self.answer_bg_xcoord,
                                                 self.answer_bg_ycoord))
            self.screen.blit(self.answers_bg_3, (answers_bg_rect.x - self.answer_bg_xcoord,
                                                 self.answer_bg_ycoord + 100))
            self.screen.blit(self.answers_bg_4, (answers_bg_rect.x + self.answer_bg_xcoord,
                                                 self.answer_bg_ycoord + 100))
            self.screen.blit(ans_letter[0], (264, 752))
            self.screen.blit(ans_letter[1], (988, 752))
            self.screen.blit(ans_letter[2], (264, 852))
            self.screen.blit(ans_letter[3], (988, 852))

        def render_answers():
            answer_text = [check_answers_length(self.answers[i]) for i in range(4)]
            answer_text_rect = [answer_text[i].get_rect() for i in range(4)]
            for i in range(4):
                answer_text_rect[i].center = self.screen_center
            self.screen.blit(answer_text[0], (answer_text_rect[0].x - self.answer_bg_xcoord, 755))
            self.screen.blit(answer_text[1], (answer_text_rect[1].x + self.answer_bg_xcoord, 755))
            self.screen.blit(answer_text[2], (answer_text_rect[2].x - self.answer_bg_xcoord, 855))
            self.screen.blit(answer_text[3], (answer_text_rect[3].x + self.answer_bg_xcoord, 855))

        def manage_hover_click(mx, my):
            manage_help_tools_click(mx, my)
            if 937 > mx > 220 and 740 < my < 790:
                if self.clicked and self.question_map[0]:
                    res = self.answers.index(self.correct) == 0
                    self.answers_bg_1 = check_answers(res)
                    show_correct_or_false(res)
                self.answers_bg_1 = pygame.image.load('res/img/answers_hover.png')
            else:
                self.answers_bg_1 = pygame.image.load('res/img/answers.png')
            if 987 < mx < 1690 and 740 < my < 790:
                if self.clicked and self.question_map[1]:
                    res = self.answers.index(self.correct) == 1
                    self.answers_bg_2 = check_answers(res)
                    show_correct_or_false(res)
                self.answers_bg_2 = pygame.image.load('res/img/answers_hover.png')
            else:
                self.answers_bg_2 = pygame.image.load('res/img/answers.png')
            if 937 > mx > 220 and 840 < my < 900:
                if self.clicked and self.question_map[2]:
                    res = self.answers.index(self.correct) == 2
                    self.answers_bg_3 = check_answers(res)
                    show_correct_or_false(res)
                self.answers_bg_3 = pygame.image.load('res/img/answers_hover.png')
            else:
                self.answers_bg_3 = pygame.image.load('res/img/answers.png')
            if 987 < mx < 1690 and 840 < my < 900:
                if self.clicked and self.question_map[3]:
                    res = self.answers.index(self.correct) == 3
                    self.answers_bg_4 = check_answers(res)
                    show_correct_or_false(res)
                self.answers_bg_4 = pygame.image.load('res/img/answers_hover.png')
            else:
                self.answers_bg_4 = pygame.image.load('res/img/answers.png')

        def start_game():
            # start the menu sound and looping
            if self.ask_name:
                ask_the_nickname()
            self.game_sound.play(-1)
            while self.game:
                mx, my = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.clicked = True
                manage_hover_click(mx, my)
                render_background()
                render_question()
                render_answers_background()
                render_answers()
                self.clicked = False
                # refresh the page
                pygame.display.flip()
                pygame.time.Clock().tick(self.fps)

        while self.game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            start_game()
            pygame.display.update()

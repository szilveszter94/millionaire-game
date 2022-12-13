import pygame, sys
from question_bank import generate_questions
from audience_graph_generator import create_random_list


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
        self.game = True
        self.correct_sound = pygame.mixer.Sound('res/sound/correct_sound.mp3')
        self.wrong_sound = pygame.mixer.Sound('res/sound/wrong_sound.mp3')
        self.gold = '#FFBF00'
        self.purple = [129, 12, 168]
        self.question_map = [True, True, True, True]
        self.questions = generate_questions()
        self.question_nr = 0
        self.answer_bg_xcoord = 360
        self.answer_bg_ycoord = 740
        self.question = self.questions[self.question_nr]['question']
        self.answers = self.questions[self.question_nr]['answers']
        self.correct = self.questions[self.question_nr]['correct']
        self.size = self.width, self.height = 1920, 1080
        self.prizes = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]
        self.y_coord = [i for i in range(498,123,-25)]
        self.white = '#ffffff'
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
        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.font_2 = pygame.font.Font('freesansbold.ttf', 24)
        self.font_3 = pygame.font.Font('freesansbold.ttf', 20)
        self.font_4 = pygame.font.Font('freesansbold.ttf', 16)
        self.help_tools = pygame.image.load('res/img/help_tools.png')
        self.remove_help = pygame.image.load('res/img/remove_help.png')
        self.answers_bg_1 = self.answers_bg_2 = self.answers_bg_3 = self.answers_bg_4 = pygame.image.load('res/img'
                                                                                                          '/answers.png')


class Game(GameUI):
    def __init__(self):
        super().__init__()

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
                self.answers_bg_1 = pygame.image.load('res/img/phone_help.png')
            if self.answers.index(self.correct) == 1:
                self.answers_bg_2 = pygame.image.load('res/img/phone_help.png')
            if self.answers.index(self.correct) == 2:
                self.answers_bg_3 = pygame.image.load('res/img/phone_help.png')
            if self.answers.index(self.correct) == 3:
                self.answers_bg_4 = pygame.image.load('res/img/phone_help.png')

        def draw_audience_result():
            ans_a = self.font_2.render("A", True, self.white)
            ans_b = self.font_2.render("B", True, self.white)
            ans_c = self.font_2.render("C", True, self.white)
            ans_d = self.font_2.render("D", True, self.white)
            self.screen.blit(ans_a, (353, 410))
            self.screen.blit(ans_b, (413, 410))
            self.screen.blit(ans_c, (473, 410))
            self.screen.blit(ans_d, (533, 410))
            pygame.draw.rect(self.screen, [20, 50 + 2 * self.random_arr[0], 50],
                             pygame.Rect(340, 400 - self.random_arr[0], 40, self.random_arr[0]))
            pygame.draw.rect(self.screen, [20, 50 + 2 * self.random_arr[1], 50],
                             pygame.Rect(400, 400 - self.random_arr[1], 40, self.random_arr[1]))
            pygame.draw.rect(self.screen, [20, 50 + 2 * self.random_arr[2], 50],
                             pygame.Rect(460, 400 - self.random_arr[2], 40, self.random_arr[2]))
            pygame.draw.rect(self.screen, [20, 50 + 2 * self.random_arr[3], 50],
                             pygame.Rect(520, 400 - self.random_arr[3], 40, self.random_arr[3]))
            pygame.draw.rect(self.screen, self.purple, pygame.Rect(340, 300, 40, 100), 1)
            pygame.draw.rect(self.screen, self.purple, pygame.Rect(400, 300, 40, 100), 1)
            pygame.draw.rect(self.screen, self.purple, pygame.Rect(460, 300, 40, 100), 1)
            pygame.draw.rect(self.screen, self.purple, pygame.Rect(520, 300, 40, 100), 1)

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
                self.game = False
                sys.exit()

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
                return self.font_4.render(ans, True, self.white)
            elif len(ans) > 40:
                return self.font_3.render(ans, True, self.white)
            else:
                return self.font_2.render(ans, True, self.white)

        def update_questions():
            if self.question_nr >= 14:
                sys.exit()
            self.question_nr += 1
            self.question = self.questions[self.question_nr]['question']
            self.answers = self.questions[self.question_nr]['answers']
            self.correct = self.questions[self.question_nr]['correct']
            self.question_map = [True, True, True, True]
            self.graph = self.show_phone_result = False

        def render_prizes():
            self.screen.blit(self.score_bg, (1390, self.y_coord[self.question_nr]))
            prize_surfaces = []
            for i in range(len(self.prizes)):
                if (i + 1) % 5 == 0:
                    color = self.white
                else:
                    color = self.gold
                item = self.font_2.render(f'{i+1}: $ {self.prizes[i]}', True, color)
                prize_surfaces.append(item)
            step = 0
            for i in range(len(prize_surfaces)):
                self.screen.blit(prize_surfaces[i], (1400, 500-step))
                step += 25

        def render_background():
            question_bg = pygame.image.load('res/img/question.png')
            question_bg_rect = question_bg.get_rect()
            question_bg_rect.center = self.screen_center
            self.screen.blit(self.bg_image, (0, 0))
            self.screen.blit(question_bg, (question_bg_rect.x, 580))
            self.screen.blit(self.help_tools, (210, 140))
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
                question_text_1 = self.font.render(splitted_question[0], True, self.white)
                question_text_2 = self.font.render(splitted_question[1], True, self.white)
                question_text_1_rect = question_text_1.get_rect()
                question_text_1_rect.center = self.screen_center
                question_text_2_rect = question_text_2.get_rect()
                question_text_2_rect.center = self.screen_center
                self.screen.blit(question_text_1, (question_text_1_rect.x, 605))
                self.screen.blit(question_text_2, (question_text_2_rect.x, 640))
            else:
                question_text = self.font.render(self.question, True, self.white)
                question_text_rect = question_text.get_rect()
                question_text_rect.center = self.screen_center
                self.screen.blit(question_text, (question_text_rect.x, 620))

        def render_answers_background():
            ans_a = self.font.render("A:", True, self.gold)
            ans_b = self.font.render("B:", True, self.gold)
            ans_c = self.font.render("C:", True, self.gold)
            ans_d = self.font.render("D:", True, self.gold)
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
            self.screen.blit(ans_a, (264, 752))
            self.screen.blit(ans_b, (988, 752))
            self.screen.blit(ans_c, (264, 852))
            self.screen.blit(ans_d, (988, 852))

        def render_answers():
            answer_text_1 = check_answers_length(self.answers[0])
            answer_text_2 = check_answers_length(self.answers[1])
            answer_text_3 = check_answers_length(self.answers[2])
            answer_text_4 = check_answers_length(self.answers[3])

            answer_text_rect_1 = answer_text_1.get_rect()
            answer_text_rect_2 = answer_text_2.get_rect()
            answer_text_rect_3 = answer_text_3.get_rect()
            answer_text_rect_4 = answer_text_4.get_rect()

            answer_text_rect_1.center = self.screen_center
            answer_text_rect_2.center = self.screen_center
            answer_text_rect_3.center = self.screen_center
            answer_text_rect_4.center = self.screen_center

            self.screen.blit(answer_text_1, (answer_text_rect_1.x - self.answer_bg_xcoord, 755))
            self.screen.blit(answer_text_2, (answer_text_rect_2.x + self.answer_bg_xcoord, 755))
            self.screen.blit(answer_text_3, (answer_text_rect_3.x - self.answer_bg_xcoord, 855))
            self.screen.blit(answer_text_4, (answer_text_rect_4.x + self.answer_bg_xcoord, 855))

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
            self.game = True
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

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            start_game()
            pygame.display.update()

import pygame, sys
from question_bank import generate_questions


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
        self.correct_sound = pygame.mixer.Sound('res/sound/correct_sound.mp3')
        self.wrong_sound = pygame.mixer.Sound('res/sound/wrong_sound.mp3')
        self.gold = '#FFBF00'
        self.question_map = [True, True, True, True]
        self.questions = generate_questions()
        self.question_nr = 0
        self.click = True
        self.answer_bg_xcoord = 360
        self.answer_bg_ycoord = 740
        self.question = self.questions[self.question_nr]['question']
        self.answers = self.questions[self.question_nr]['answers']
        self.correct = self.questions[self.question_nr]['correct']
        self.size = self.width, self.height = 1920, 1080
        self.white = '#ffffff'
        self.half_cut = self.phone = self.audience = False
        self.bg_image = pygame.image.load('res/img/bg_image.png')
        self.screen = pygame.display.set_mode(self.size)
        self.screen_center = self.screen.get_rect().center
        self.game_sound = pygame.mixer.Sound('res/sound/game_sound.mp3')
        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.font_2 = pygame.font.Font('freesansbold.ttf', 24)
        self.font_3 = pygame.font.Font('freesansbold.ttf', 20)
        self.font_4 = pygame.font.Font('freesansbold.ttf', 16)
        self.help_tools = pygame.image.load('res/img/help_tools.png')
        self.remove_help = pygame.image.load('res/img/remove_help.png')
        self.answers_bg_1 = self.answers_bg_2 = self.answers_bg_3 = self.answers_bg_4 = pygame.image.load('res/img'
                                                                                                          '/answers.png')

    def manage_help_tools_click(self, mx, my, click):
        if click:
            if 361 > mx > 212 and 143 < my < 237 and not self.half_cut:
                self.half_cut = True
                self.half_cut_function()
            if 524 > mx > 375 and 143 < my < 237 and not self.phone:
                self.phone = True
            if 686 > mx > 536 and 143 < my < 237 and not self.audience:
                self.audience = True

    def half_cut_function(self):
        two_bad = self.questions[self.question_nr]['two_bad']
        for i in range(len(self.answers)):
            if self.answers[i] in two_bad:
                self.answers[i] = ""
                self.question_map[i] = False

    def show_correct_or_false(self, res):
        self.render_answers_background()
        self.render_answers()
        pygame.display.flip()
        if res:
            self.correct_sound.play(1)
            pygame.time.wait(2000)
            self.correct_sound.stop()
        else:
            self.wrong_sound.play(1)
            pygame.time.wait(2000)
            self.wrong_sound.stop()
        self.update_questions()

    def render_background(self):
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

    def manage_question_length(self):
        words = [word.split(' ') for word in self.question.splitlines()]
        all_word = words[0]
        length = len(all_word) // 2
        first = all_word[0:length]
        second = all_word[length:len(all_word)]
        return [" ".join(first), " ".join(second)]

    def render_question(self):
        if len(self.question) > 86:
            splitted_question = self.manage_question_length()
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

    def update_questions(self):
        if self.question_nr >= 14:
            sys.exit()
        self.question_nr += 1
        self.question = self.questions[self.question_nr]['question']
        self.answers = self.questions[self.question_nr]['answers']
        self.correct = self.questions[self.question_nr]['correct']
        self.question_map = [True, True, True, True]

    def render_answers_background(self):
        answers_bg_rect = self.answers_bg_1.get_rect()
        answers_bg_rect.center = self.screen_center
        ans_a = self.font.render("A:", True, self.gold)
        ans_b = self.font.render("B:", True, self.gold)
        ans_c = self.font.render("C:", True, self.gold)
        ans_d = self.font.render("D:", True, self.gold)
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

    def check_answers_length(self, ans):
        if len(ans) > 60:
            return self.font_4.render(ans, True, self.white)
        elif len(ans) > 40:
            return self.font_3.render(ans, True, self.white)
        else:
            return self.font_2.render(ans, True, self.white)

    def render_answers(self):
        answer_text_1 = self.check_answers_length(self.answers[0])
        answer_text_2 = self.check_answers_length(self.answers[1])
        answer_text_3 = self.check_answers_length(self.answers[2])
        answer_text_4 = self.check_answers_length(self.answers[3])

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


class Game(GameUI):
    def __init__(self):
        super().__init__()

        def manage_hover_click(mx, my, click):
            self.manage_help_tools_click(mx, my, click)
            if 937 > mx > 220 and 740 < my < 790:
                if click and self.question_map[0]:
                    res = self.answers.index(self.correct) == 0
                    self.answers_bg_1 = check_answers(res)
                    self.show_correct_or_false(res)
                self.answers_bg_1 = pygame.image.load('res/img/answers_hover.png')
            else:
                self.answers_bg_1 = pygame.image.load('res/img/answers.png')
            if 987 < mx < 1690 and 740 < my < 790:
                if click and self.question_map[1]:
                    res = self.answers.index(self.correct) == 1
                    self.answers_bg_2 = check_answers(res)
                    self.show_correct_or_false(res)
                self.answers_bg_2 = pygame.image.load('res/img/answers_hover.png')
            else:
                self.answers_bg_2 = pygame.image.load('res/img/answers.png')
            if 937 > mx > 220 and 840 < my < 900:
                if click and self.question_map[2]:
                    res = self.answers.index(self.correct) == 2
                    self.answers_bg_3 = check_answers(res)
                    self.show_correct_or_false(res)
                self.answers_bg_3 = pygame.image.load('res/img/answers_hover.png')
            else:
                self.answers_bg_3 = pygame.image.load('res/img/answers.png')
            if 987 < mx < 1690 and 840 < my < 900:
                if click and self.question_map[3]:
                    res = self.answers.index(self.correct) == 3
                    self.answers_bg_4 = check_answers(res)
                    self.show_correct_or_false(res)
                self.answers_bg_4 = pygame.image.load('res/img/answers_hover.png')
            else:
                self.answers_bg_4 = pygame.image.load('res/img/answers.png')

        def start_game():
            # start the menu sound and looping
            game = True
            self.game_sound.play(-1)
            while game:
                mx, my = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        manage_hover_click(mx, my, True)
                manage_hover_click(mx, my, False)
                self.render_background()
                self.render_question()
                self.render_answers_background()
                self.render_answers()
                # refresh the page
                pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            start_game()
            pygame.display.update()

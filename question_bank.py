import requests
import html
import random


def generate_questions():
    response_easy = requests.get('https://opentdb.com/api.php?amount=5&difficulty=easy&type=multiple')
    response_medium = requests.get('https://opentdb.com/api.php?amount=5&difficulty=medium&type=multiple')
    response_hard = requests.get('https://opentdb.com/api.php?amount=5&difficulty=hard&type=multiple')

    questions = []

    easy = response_easy.json()['results']
    medium = response_medium.json()['results']
    hard = response_hard.json()['results']
    for i in range(15):
        step = 0
        difficulty = easy
        if i >= 10:
            step = 10
            difficulty = medium
        elif i >= 5:
            step = 5
            difficulty = hard
        question = html.unescape(difficulty[i - step]['question'])
        answers = difficulty[i - step]['incorrect_answers']
        answers = [html.unescape(i) for i in answers]
        correct = html.unescape(difficulty[i - step]['correct_answer'])
        answers.append(correct)
        random.shuffle(answers)
        questions.append({"question": question, "answers": answers, "correct": correct})
    return questions


import json
import datetime


def update_scores(score, high_scores, today):
    newlist = sorted(high_scores, key=lambda d: d['val'])
    for i in range(len(newlist) - 1, -1, -1):
        if newlist[i]['val'] < score[1]:
            score[1], newlist[i]['val'] = newlist[i]['val'], score[1]
            score[0], newlist[i]['name'] = newlist[i]['name'], score[0]
            today, newlist[i]['date'] = newlist[i]['date'], today
    return newlist


def write_highscore(score):
    today = datetime.datetime.today().strftime("%Y.%m.%d")
    with open('res/data/highscores', "r") as file:
        highscores = update_scores(score, json.load(file), today)

    with open("res/data/highscores", "w") as file:
        json.dump(highscores, file, indent=4)


def read_highscores():
    with open('res/data/highscores', "r") as file:
        highscores = json.load(file)
        return highscores[::-1]


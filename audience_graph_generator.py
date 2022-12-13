import random


def create_random_list(incorrect_answers, correct):
    rand_num = [random.choice(range(0, 100)) for r in range(4)]  # create random integers
    rand_num = [int(i / sum(rand_num) * 100) for i in rand_num]
    index = incorrect_answers.index(correct)
    index_2 = rand_num.index(max(rand_num))
    if index != index_2:
        rand_num[index], rand_num[index_2] = rand_num[index_2], rand_num[index]
    return rand_num

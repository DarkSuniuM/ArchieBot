"""
Utils file.

Functions that are getting used by
direct handlers are defined here!
"""

from random import randint, sample, shuffle
from telegram import InlineKeyboardButton

def captcha_generator(user_id, group_id):
    """Generate captcha."""
    first_operator = 2
    second_operator = randint(1, 10)
    correct_answer = first_operator * second_operator
    equation = f"{first_operator} * {second_operator}"
    all_answers = answer_generator(correct_answer, 4)
    inline_buttons = []
    for answer in all_answers:
        data = f"{user_id},{group_id},{int(answer == correct_answer) or -answer}"
        button = InlineKeyboardButton(answer, callback_data=data)
        inline_buttons.append(button)
    return (equation, correct_answer, inline_buttons)


def answer_generator(correct_answer, length):
    """Generate captcha answers."""
    first_list = list(range(0, correct_answer))
    second_list = list(range(correct_answer + 1, length))
    random_generated_list = sample(first_list + second_list, length - 1)
    random_generated_list.append(correct_answer)
    shuffle(random_generated_list)
    return random_generated_list

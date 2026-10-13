import random
import string

def ask_length(question):
    while True:
        try:
            answer = int(input(question))
            if answer > 0:
                return answer
        except ValueError:
            print("Введите число")
            continue

def ask_yes_no(question):
    while True:
        answer = input(question)
        if answer.lower() == "y":
            return True
        elif answer.lower() == "n":
            return False
        print("Введите y или n!")

def build_charset():
    chosen_sets = []

    if ask_yes_no("Буквы в нижнем регистре? (y/n): "):
        chosen_sets.append(string.ascii_lowercase)

    if ask_yes_no("Буквы в верхнем регистре? (y/n): "):
        chosen_sets.append(string.ascii_uppercase)

    if ask_yes_no("Цифры? (y/n): "):
        chosen_sets.append(string.digits)

    if ask_yes_no("Спецсимволы? (y/n): "):
        chosen_sets.append(string.punctuation)

    return chosen_sets

def generate_password(length, chosen_sets):
    password_chars = []

    for s in chosen_sets:
        password_chars.append(random.choice(s))

    all_chars = "".join(chosen_sets)
    while len(password_chars) < length:
        password_chars.append(random.choice(all_chars))

    random.shuffle(password_chars)
    return "".join(password_chars)

def get_rate_password(password, chosen_sets):
    password_len = len(password)
    score = 0

    if password_len >= 8:
        if password_len <= 11:
            score += 1
        elif password_len <= 15:
            score += 2
        else:
            score += 3

        score += sum(any(c in password for c in rule) for rule in chosen_sets)

    if score <= 1:
        return "Слабый пароль"
    elif score <= 4:
        return "Средний пароль"
    else:
        return "Сложный пароль"



def main():
    length = ask_length("Длина пароля: ")
    chosen_sets = build_charset()
    if not chosen_sets:
        print("Не выбрано ни одного типа!")
        return
    password = generate_password(length, chosen_sets)
    rate_password = get_rate_password(password, chosen_sets)
    print(password)
    print(rate_password)

main()

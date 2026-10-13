import random
import string
def generate_password():
    try:
        length = int(input("Длина пароля1: "))
    except ValueError:
        print("Ошибка: введите число.")
        return
    if length < 1:
        print("Ошибка: длина должна быть не менее 1 символа.")
        return
    choices = {
        "1": string.ascii_uppercase,
        "2": string.ascii_lowercase,
        "3": string.digits,
        "4": string.punctuation,
    }
    print(
        "Выбор (через пробел, например: 1 2 3):\n1: A-Z | 2: a-z | 3: 0-9 | 4: !@#$"
    )
    user_choice = input("Введите номера: ").split()
    pools = [choices[i] for i in user_choice if i in choices]
    if not pools:
        print("Ошибка: вы ничего не выбрали.")
        return
    all_chars = "".join(pools)
    password = [random.choice(all_chars) for _ in range(length)]
    random.shuffle(password)
    print(f"Пароль: {''.join(password)}")
if __name__ == "__main__":
    generate_password()

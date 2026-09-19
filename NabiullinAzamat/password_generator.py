import secrets
import string

# Набиуллин Азамат 24111 2026 Проект 2


def main() -> None:
    symbol_types = [string.ascii_lowercase]
    alphabet = string.ascii_lowercase
    print("Какие символы использовать при генерации пароля?")
    if input("Заглавные буквы? y/n: ") == "y":
        symbol_types.append(string.ascii_uppercase)
        alphabet += string.ascii_uppercase
    if input("Цифры? y/n: ") == "y":
        symbol_types.append(string.digits)
        alphabet += string.digits
    if input("Специальные символы? y/n: ") == "y":
        symbol_types.append(string.punctuation)
        alphabet += string.punctuation

    length = 0
    min_length = len(symbol_types)
    while length < min_length:
        try:
            length = int(input(f"Длина пароля (минимум {min_length} символов): "))
        except ValueError:
            print("Длина пароля должна быть целым числом! Попробуйте еще раз")

    password = ""
    while True:
        for i in range(length):
            password += secrets.choice(alphabet)

        # Проверяем имеется ли в пароле хотя бы один символ каждого типа
        success = True
        for symbol_type in symbol_types:
            success = success and any(char in password for char in symbol_type)

        if success:
            break
        else:
            password = ""

    print(f"Сгенерированый пароль: {password}")


if __name__ == "__main__":
    main()

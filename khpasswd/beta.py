import random

char_types = {
    "upper_case_letter": "upper_case",
    "lower_case_letter": "lower_case",
    "special_char": "special_char",
}

special_chars = (
    "!", "#", "$", "%", "&", "(", ")", "*", "+", ",", 
    "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", 
    "[", "\\", "]", "^", "_", "{", "|", "}", "~"
)


def get_rand_sym(char_type: str) -> str:
    if (char_type == char_types["upper_case_letter"]):
        return chr(random.randint(65, 90))
    elif (char_type == char_types["lower_case_letter"]):
        return chr(random.randint(97, 122))
    elif (char_type == char_types["special_char"]):
        return random.choice(special_chars)

def describe_sym(char: str) -> str:
    if (65 <= ord(char) <= 90):
        return char_types["upper_case_letter"]
    if (97 <= ord(char) <= 122):
        return char_types["lower_case_letter"]
    else:
        return char_types["special_char"]
    


def create_passwd(length: int) -> str: # Лучше не использовать len как имя переменной, это встроенная функция
    res = list()
    for i in range(length):
        param = random.choice((char_types["lower_case_letter"], char_types["special_char"], char_types["upper_case_letter"]))
        char = get_rand_sym(param)
        res.append(char)
    return "".join(res)
    

def correct_passwd(passwd: str) -> str:
    if len(passwd) <= 6:
        return passwd
    has_upper = 0
    has_lower = 0
    has_special = 0
    
    cpy_passwd = list(passwd) 
    
    for i in cpy_passwd:
        if describe_sym(i) == char_types["upper_case_letter"]:
            has_upper += 1
        if describe_sym(i) == char_types["lower_case_letter"]:
            has_lower += 1
        if describe_sym(i) == char_types["special_char"]:
            has_special += 1
            
    if has_upper > 0 and has_lower > 0 and has_special > 0:
        return "".join(cpy_passwd)
    
    if has_upper == 0:
        biggest = char_types["lower_case_letter"] if has_lower > has_special else char_types["special_char"]
        for idx, char in enumerate(cpy_passwd):
            if biggest == describe_sym(char):
                cpy_passwd[idx] = get_rand_sym(char_types["upper_case_letter"]) # Заменяем на то, чего не хватало!
                break

    if has_lower == 0:
        biggest = char_types["upper_case_letter"] if has_upper > has_special else char_types["special_char"]
        for idx, char in enumerate(cpy_passwd):
            if biggest == describe_sym(char):
                cpy_passwd[idx] = get_rand_sym(char_types["lower_case_letter"])
                break

    if has_special == 0:
        biggest = char_types["upper_case_letter"] if has_upper > has_lower else char_types["lower_case_letter"]
        for idx, char in enumerate(cpy_passwd):
            if biggest == describe_sym(char):
                cpy_passwd[idx] = get_rand_sym(char_types["special_char"]) # Заменяем на то, чего не хватало!
                break
                
    return "".join(cpy_passwd)

def get_passwd(length: int) -> str:
    res = create_passwd(length)
    res = correct_passwd(res)
    return res


print(get_passwd(10))

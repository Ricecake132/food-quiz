def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("내용을 입력해 주세요.")


def read_number(prompt, maximum):
    while True:
        try:
            number = int(read_text(prompt))
        except ValueError:
            print("숫자를 입력해 주세요.")
            continue
        if 1 <= number <= maximum:
            return number
        print(f"1~{maximum} 사이의 번호를 입력해 주세요.")

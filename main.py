from inputs import read_number


def run():
    while True:
        print("\n일본 음식 이름 맞히기")
        print("1. 퀴즈 풀기   2. 퀴즈 추가   3. 퀴즈 목록   4. 점수 확인   5. 종료")
        choice = read_number("선택: ", 5)
        if choice == 5:
            break
        print("준비 중인 기능입니다.")


if __name__ == "__main__":
    run()

from quiz import Quiz
from inputs import read_number, read_text
from questions import default_quizzes


def play(quizzes):
    if not quizzes:
        print("등록된 문제가 없습니다.")
        return
    correct = 0
    for index, quiz in enumerate(quizzes, start=1):
        print(f"\n[문제 {index}/{len(quizzes)}]")
        quiz.display()
        if quiz.is_correct(read_number("정답 번호: ", 4)):
            print("정답입니다!")
            correct += 1
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번 {quiz.choices[quiz.answer - 1]}입니다.")
    score = round(correct * 100 / len(quizzes))
    print(f"결과: {len(quizzes)}문제 중 {correct}개 정답 ({score}점)")
    return score


def add_quiz(quizzes):
    question = read_text("문제: ")
    choices = [read_text(f"선택지 {index}: ") for index in range(1, 5)]
    answer = read_number("정답 번호: ", 4)
    quizzes.append(Quiz(question, choices, answer))
    print("퀴즈를 추가했습니다.")


def run():
    quizzes = default_quizzes()
    while True:
        print("\n일본 음식 이름 맞히기")
        print("1. 퀴즈 풀기   2. 퀴즈 추가   3. 퀴즈 목록   4. 점수 확인   5. 종료")
        choice = read_number("선택: ", 5)
        if choice == 5:
            break
        if choice == 1:
            play(quizzes)
            continue
        if choice == 2:
            add_quiz(quizzes)
            continue
        print("준비 중인 기능입니다.")


if __name__ == "__main__":
    run()

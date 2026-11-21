from quiz import Quiz
from inputs import read_number, read_text
from questions import default_quizzes


class QuizGame:
    def __init__(self):
        self.quizzes = default_quizzes()
        self.best_score = None

    def play(self):
        if not self.quizzes:
            print("등록된 문제가 없습니다.")
            return
        correct = 0
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {index}/{len(self.quizzes)}]")
            quiz.display()
            if quiz.is_correct(read_number("정답 번호: ", 4)):
                print("정답입니다!")
                correct += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번 {quiz.choices[quiz.answer - 1]}입니다.")
        score = round(correct * 100 / len(self.quizzes))
        print(f"결과: {len(self.quizzes)}문제 중 {correct}개 정답 ({score}점)")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("최고 점수를 갱신했습니다.")


    def add_quiz(self):
        question = read_text("문제: ")
        choices = [read_text(f"선택지 {index}: ") for index in range(1, 5)]
        answer = read_number("정답 번호: ", 4)
        self.quizzes.append(Quiz(question, choices, answer))
        print("퀴즈를 추가했습니다.")


    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 문제가 없습니다.")
            return
        print(f"등록된 퀴즈 {len(self.quizzes)}개")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")

    def show_score(self):
        if self.best_score is None:
            print("아직 풀이 기록이 없습니다.")
        else:
            print(f"최고 점수: {self.best_score}점")

    def run(self):
        while True:
            print("\n일본 음식 이름 맞히기")
            print("1. 퀴즈 풀기   2. 퀴즈 추가   3. 퀴즈 목록   4. 점수 확인   5. 종료")
            choice = read_number("선택: ", 5)
            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            else:
                break


if __name__ == "__main__":
    QuizGame().run()

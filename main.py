import argparse
import json
import random
from pathlib import Path
from tempfile import NamedTemporaryFile

from quiz import Quiz
from inputs import read_number, read_text
from questions import default_quizzes


STATE_FILE = Path(__file__).with_name("state.json")


class QuizGame:
    def __init__(self, shuffle=False):
        self.shuffle = shuffle
        self.quizzes = default_quizzes()
        self.best_score = None
        self.dirty = False

    def load(self):
        try:
            with STATE_FILE.open(encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
                raise ValueError("퀴즈 목록 오류")
            score = data["best_score"]
            if score is not None and (type(score) is not int or not 0 <= score <= 100):
                raise ValueError("점수 범위 오류")
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            self.best_score = score
            print(f"저장된 퀴즈 {len(self.quizzes)}개를 불러왔습니다.")
        except FileNotFoundError:
            self.dirty = True
        except (ValueError, KeyError, RecursionError):
            print("저장 파일이 손상되어 기본 퀴즈로 초기화합니다.")
            self.dirty = True
        except OSError as error:
            print(f"파일을 읽을 수 없어 기본 퀴즈로 시작합니다. {error}")

    def save(self):
        if not self.dirty:
            return
        data = {"quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_score": self.best_score}
        temporary = None
        try:
            with NamedTemporaryFile(mode="w", encoding="utf-8", dir=STATE_FILE.parent,
                                    prefix=".state-", suffix=".tmp", delete=False) as file:
                temporary = Path(file.name)
                json.dump(data, file, ensure_ascii=False, indent=2)
            temporary.replace(STATE_FILE)
            self.dirty = False
        except OSError as error:
            print(f"저장에 실패했습니다. {error}")
        finally:
            if temporary is not None and temporary.exists():
                try:
                    temporary.unlink()
                except OSError:
                    pass

    def play(self):
        if not self.quizzes:
            print("등록된 문제가 없습니다.")
            return
        correct = 0
        questions = self.quizzes.copy()
        if self.shuffle:
            random.shuffle(questions)
        for index, quiz in enumerate(questions, start=1):
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
            self.dirty = True
            self.save()
            print("최고 점수를 갱신했습니다.")

    def add_quiz(self):
        question = read_text("문제: ")
        choices = [read_text(f"선택지 {index}: ") for index in range(1, 5)]
        answer = read_number("정답 번호: ", 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.dirty = True
        self.save()
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
    parser = argparse.ArgumentParser(description="일본 음식 이름 맞히기")
    parser.add_argument("--shuffle", action="store_true", help="매 게임마다 문제 순서를 섞습니다.")
    game = QuizGame(shuffle=parser.parse_args().shuffle)
    try:
        game.load()
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되었습니다. 완료된 변경 사항을 저장합니다.")
    finally:
        game.save()
        print("게임을 종료합니다.")

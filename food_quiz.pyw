"""Desktop interface for the Japanese food quiz (Windows: double-click this file)."""
import random
import tkinter as tk
from contextlib import redirect_stdout
from io import StringIO
from tkinter import messagebox, ttk

from main import QuizGame
from quiz import Quiz


class QuizWindow:
    def __init__(self, root):
        self.root = root
        root.title("일본 음식 이름 맞히기")
        root.geometry("630x540")
        root.minsize(480, 480)
        self.body = ttk.Frame(root, padding=24)
        self.body.pack(fill="both", expand=True)
        self.game = QuizGame()
        self.shuffle = tk.BooleanVar(value=False)
        with redirect_stdout(StringIO()) as status:
            self.game.load()
        self.home()
        notice = status.getvalue().strip()
        if notice and not notice.startswith("저장된 퀴즈"):
            messagebox.showwarning("저장 파일", notice, parent=root)
        root.protocol("WM_DELETE_WINDOW", self.close)

    def page(self, title):
        for child in self.body.winfo_children():
            child.destroy()
        ttk.Label(self.body, text=title, font=("Malgun Gothic", 19, "bold"),
                  wraplength=420).pack(anchor="w", pady=(0, 14))

    def button(self, label, command):
        button = ttk.Button(self.body, text=label, command=command)
        button.pack(fill="x", pady=3, ipady=4)
        return button

    def home(self):
        self.page("일본 음식 이름 맞히기")
        score = "첫 게임 전" if self.game.best_score is None else f"{self.game.best_score}점"
        ttk.Label(self.body, text=f"등록된 문제 {len(self.game.quizzes)}개   ·   최고 점수 {score}").pack(anchor="w")
        ttk.Checkbutton(self.body, text="문제 순서 섞기", variable=self.shuffle).pack(anchor="w", pady=12)
        self.button("퀴즈 풀기", self.start)
        self.button("새 문제 등록", self.add)
        self.button("문제 목록", self.list_questions)
        self.button("종료", self.close)

    def persist(self):
        with redirect_stdout(StringIO()) as status:
            self.game.save()
        if self.game.dirty:
            messagebox.showwarning("저장 실패", status.getvalue().strip(), parent=self.root)
        return not self.game.dirty

    def close(self):
        if self.persist() or messagebox.askyesno("종료", "저장하지 못한 변경이 있습니다. 종료할까요?", parent=self.root):
            self.root.destroy()

    def start(self):
        self.questions = self.game.quizzes.copy()
        if not self.questions:
            messagebox.showinfo("퀴즈 풀기", "먼저 문제를 등록해 주세요.", parent=self.root)
            return
        if self.shuffle.get():
            random.shuffle(self.questions)
        self.index = 0
        self.correct = 0
        self.question()

    def question(self):
        quiz = self.questions[self.index]
        self.page(f"문제 {self.index + 1} / {len(self.questions)}")
        ttk.Label(self.body, text=quiz.question, wraplength=420).pack(anchor="w", pady=(0, 12))
        self.options = []
        for number, choice in enumerate(quiz.choices, 1):
            self.options.append(self.button(f"{number}. {choice}", lambda n=number: self.answer(n)))
        self.feedback = ttk.Label(self.body, wraplength=420)
        self.feedback.pack(anchor="w", pady=8)

    def answer(self, number):
        quiz = self.questions[self.index]
        for option in self.options:
            option.state(["disabled"])
        if quiz.is_correct(number):
            self.correct += 1
            self.feedback.configure(text="정답입니다!")
        else:
            self.feedback.configure(text=f"정답은 {quiz.answer}번 {quiz.choices[quiz.answer - 1]}입니다.")
        self.index += 1
        if self.index < len(self.questions):
            self.button("다음 문제", self.question)
        else:
            total = len(self.questions)
            score = round(self.correct * 100 / total)
            if self.game.best_score is None or score > self.game.best_score:
                self.game.best_score = score
                self.game.dirty = True
                self.persist()
            ttk.Label(self.body, text=f"{total}문제 중 {self.correct}개 정답 · {score}점").pack(anchor="w")
            self.button("메뉴로", self.home)

    def list_questions(self):
        self.page(f"문제 목록 · {len(self.game.quizzes)}개")
        box = tk.Text(self.body, wrap="word", height=10)
        box.pack(fill="both", expand=True)
        for number, quiz in enumerate(self.game.quizzes, 1):
            box.insert("end", f"{number}. {quiz.question}\n\n")
        box.configure(state="disabled")
        self.button("메뉴로", self.home)

    def add(self):
        self.page("새 문제 등록")
        fields = []
        for label in ["문제", "보기 1", "보기 2", "보기 3", "보기 4"]:
            ttk.Label(self.body, text=label).pack(anchor="w")
            entry = ttk.Entry(self.body)
            entry.pack(fill="x", pady=(0, 4))
            fields.append(entry)
        fields[0].focus_set()
        ttk.Label(self.body, text="정답 번호").pack(anchor="w")
        answer = ttk.Combobox(self.body, values=("1", "2", "3", "4"), state="readonly")
        answer.pack(fill="x")

        def register():
            values = [field.get().strip() for field in fields]
            if not all(values) or not answer.get():
                messagebox.showinfo("입력 확인", "문제와 보기 네 개를 입력하고 정답 번호를 고르세요.", parent=self.root)
                return
            self.game.quizzes.append(Quiz(values[0], values[1:], int(answer.get())))
            self.game.dirty = True
            self.persist()
            self.list_questions()

        self.button("등록", register)
        self.button("취소", self.home)


if __name__ == "__main__":
    window = tk.Tk()
    QuizWindow(window)
    window.mainloop()

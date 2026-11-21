class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"  {number}. {choice}")

    def is_correct(self, number):
        return number == self.answer

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("문제 형식 오류")
        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")
        if not isinstance(question, str) or not question.strip():
            raise ValueError("빈 문제")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지 개수 오류")
        if not all(isinstance(item, str) and item.strip() for item in choices):
            raise ValueError("빈 선택지")
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답 번호 오류")
        return cls(question, choices, answer)

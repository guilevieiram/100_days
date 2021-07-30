from model import Model, MyModel
from view import View, TerminalView, TkView
import time

# Controller class for the quizzer app

class Quizzer:

    def __init__(self, model: Model, view: View, number_questions: int = 10) -> None:

        self.score: int = 0
        self.question_number: int = 1
        self.question: str = ""
        self.answer: bool = ""
        
        self.model: Model = model(
            number_questions=number_questions
            )

        self.max_number_questions: int = self.model.get_max_number_questions()

        self.view: View = view(
            input_action=self.input_action
            )

        self.update_score()
        self.show_question()
        self.view.show_screen()

    def show_question(self) -> None:
        self.question: str = self.model.get_question()
        self.view.show_question(question=self.question, number=self.question_number)

    def input_action(self, answer) -> bool:
        self.answer = answer

        self.check_answer_is_right()

        if not self.is_over():
            self.question_number += 1
            self.update_score()
            self.show_question()

    def check_answer_is_right(self) -> None:
        right_answer: bool = self.model.get_answer(question=self.question)
        if self.answer == right_answer:
            self.score += 1
            self.view.right_answer()
        else:
            self.view.wrong_answer()

    def update_score(self) -> None:
        self.view.update_score(score=self.score, max_score=self.max_number_questions)
 
    def is_over(self) -> bool:
        if self.model.are_questions_over():
            self.end_game()
            return True
        else:
            return False

    def end_game(self) -> None:
        self.view.end_screen(score=self.score, max_score=self.max_number_questions)


def main() -> None:

    # Bridge pattern for the controller model view design
    quizzer = Quizzer(
        view = TkView,
        model = MyModel,
        number_questions=10
        )

if __name__ == "__main__":
    main()
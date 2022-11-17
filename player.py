from questions import Question

class Game:

    def __init__(self):
        self.token = Question.getSessionToken()
        self.categories = Question.getCategories()
        self.category = None
        self.difficulty = None


    def setCategory(self, cat: int) -> None:
        self.category = cat
        print(self.category)


    def setDifficulty(self, diff: str) -> None:
        self.difficulty = diff
        print(self.difficulty)


    def getNewQuestion(self) -> Question:
        self.question = Question(diff=self.difficulty, cat=self.category, token=self.token)
        # self.question.translateQ()
        return self.question

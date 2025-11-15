# quiz/models.py

from django.db import models


class Question(models.Model):
    question = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=500)
    sub_topic = models.CharField(max_length=200)
    quiz_set = models.CharField(max_length=50)

    def __str__(self):
        return self.question[:50]

    def get_options(self):
        """Returns a list of all answer options"""
        return [
            ("A", self.option_a),
            ("B", self.option_b),
            ("C", self.option_c),
            ("D", self.option_d),
        ]

    def is_correct(self, answer):
        """Check if the given answer is correct"""
        return answer == self.correct_answer

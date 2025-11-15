# quiz/management/commands/load_questions.py

import csv
from django.core.management.base import BaseCommand
from quiz.models import Question


class Command(BaseCommand):
    help = "Load questions from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        # Clear existing questions
        Question.objects.all().delete()

        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            count = 0

            for row in reader:
                Question.objects.create(
                    question=row["question"],
                    option_a=row["option_a"],
                    option_b=row["option_b"],
                    option_c=row["option_c"],
                    option_d=row["option_d"],
                    correct_answer=row["correct_answer"],
                    sub_topic=row["sub_topic"],
                    quiz_set=row["quiz_set"],
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {count} questions"))

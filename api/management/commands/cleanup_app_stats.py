import pandas as pd

from django.core.management import BaseCommand

from api.models import (
    Question,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    DailyStat,
)


def cleanup_question_answer_events():
    """
    cleanup QuestionAnswerEvent
    """
    print("===== starting QuestionAnswerEvent cleanup")

    question_stats = QuestionAnswerEvent.objects.all()
    question_stats_df = pd.DataFrame.from_records(question_stats.values())
    print(f"{question_stats_df.shape[0]} items")

    if question_stats_df.shape[0]:
        # aggregate by question_id
        question_id_list = question_stats_df["question_id"].unique()
        print(f"{len(question_id_list)} unique questions")

        # loop on unique question ids
        for question_id in question_id_list:
            question = Question.objects.get(pk=question_id)
            question_id_df = question_stats_df[
                question_stats_df["question_id"] == question_id
            ]
            # # get number of stats
            # question_id_stat_count = question_id_df.shape[0]
            # get number of stats per type
            question_id_answer_count = question_id_df.shape[0]
            question_id_answer_correct_count = question_id_df[
                question_id_df["choice"] == question.answer_correct
            ].shape[0]
            # update question
            question.answer_count += question_id_answer_count
            question.answer_success_count += question_id_answer_correct_count
            # save question
            question.save()

        # aggregate by day / hour
        question_stats_df["created_date"] = [
            d.date() for d in question_stats_df["created"]
        ]
        question_stats_df["created_hour"] = [
            d.time().hour for d in question_stats_df["created"]
        ]
        # get list of unique dates
        date_list = question_stats_df["created_date"].unique()
        print(f"{len(date_list)} unique dates")

        # loop on unique dates
        for date_unique in date_list:
            daily_stat, created = DailyStat.objects.get_or_create(date=date_unique)
            date_df = question_stats_df[
                question_stats_df["created_date"] == date_unique
            ]
            # get number of stats
            date_stat_count = date_df.shape[0]
            date_stat_from_quiz_count = date_df[date_df["source"] == "quiz"].shape[0]
            # update daily stat
            daily_stat.question_answer_count += date_stat_count
            daily_stat.question_answer_from_quiz_count += date_stat_from_quiz_count

            # get list of unique date hours
            date_hour_list = date_df["created_hour"].unique()
            # loop on unique hours
            for date_hour_unique in date_hour_list:
                date_hour_df = date_df[date_df["created_hour"] == date_hour_unique]
                # get number of stats
                date_hour_stat_count = date_hour_df.shape[0]
                date_hour_stat_from_quiz_count = date_hour_df[
                    date_hour_df["source"] == "quiz"
                ].shape[0]
                # update question
                daily_stat.hour_split[str(date_hour_unique)][
                    "question_answer_count"
                ] += date_hour_stat_count
                daily_stat.hour_split[str(date_hour_unique)][
                    "question_answer_from_quiz_count"
                ] += date_hour_stat_from_quiz_count

            # save daily stat
            daily_stat.save()

        # delete all processed question_stats
        question_stats.delete()
        print("QuestionAnswerEvent deleted")


def cleanup_question_feedback_events():
    """
    cleanup QuestionFeedbackEvent
    """
    print("===== starting QuestionFeedbackEvent cleanup")

    question_feedbacks = QuestionFeedbackEvent.objects.all()
    question_feedbacks_df = pd.DataFrame.from_records(question_feedbacks.values())
    print(f"{question_feedbacks_df.shape[0]} items")

    if question_feedbacks_df.shape[0]:
        # aggregate by question_id
        question_id_list = question_feedbacks_df["question_id"].unique()
        print(f"{len(question_id_list)} unique questions")

        # loop on unique question ids
        for question_id in question_id_list:
            question = Question.objects.get(pk=question_id)
            question_id_df = question_feedbacks_df[
                question_feedbacks_df["question_id"] == question_id
            ]
            # # get number of feedbacks
            # question_id_feedback_count = question_id_df.shape[0]
            # get number of feedbacks per type
            question_id_like_count = question_id_df[
                question_id_df["choice"] == "like"
            ].shape[0]
            question_id_dislike_count = question_id_df[
                question_id_df["choice"] == "dislike"
            ].shape[0]
            # update question
            question.like_count += question_id_like_count
            question.dislike_count += question_id_dislike_count
            # save question
            question.save()

        # aggregate by day / hour
        question_feedbacks_df["created_date"] = [
            d.date() for d in question_feedbacks_df["created"]
        ]
        question_feedbacks_df["created_hour"] = [
            d.time().hour for d in question_feedbacks_df["created"]
        ]
        # get list of unique dates
        date_list = question_feedbacks_df["created_date"].unique()
        print(f"{len(date_list)} unique dates")

        # loop on unique dates
        for date_unique in date_list:
            daily_stat, created = DailyStat.objects.get_or_create(date=date_unique)
            date_df = question_feedbacks_df[
                question_feedbacks_df["created_date"] == date_unique
            ]
            # get number of feedbacks
            date_feedback_count = date_df.shape[0]
            date_feedback_from_quiz_count = date_df[date_df["source"] == "quiz"].shape[
                0
            ]
            # update daily stat
            daily_stat.question_feedback_count += date_feedback_count
            daily_stat.question_feedback_from_quiz_count += (
                date_feedback_from_quiz_count
            )

            # get list of unique date hours
            date_hour_list = date_df["created_hour"].unique()
            # loop on unique hours
            for date_hour_unique in date_hour_list:
                date_hour_df = date_df[date_df["created_hour"] == date_hour_unique]
                # get number of feedbacks
                date_hour_feedback_count = date_hour_df.shape[0]
                date_hour_feedback_from_quiz_count = date_hour_df[
                    date_hour_df["source"] == "quiz"
                ].shape[0]
                # update daily stat
                daily_stat.hour_split[str(date_hour_unique)][
                    "question_feedback_count"
                ] += date_hour_feedback_count
                daily_stat.hour_split[str(date_hour_unique)][
                    "question_feedback_from_quiz_count"
                ] += date_hour_feedback_from_quiz_count

            # save daily stat
            daily_stat.save()

        # delete all processed question_feedbacks
        question_feedbacks.delete()
        print("QuestionFeedbackEvent deleted")


def cleanup_quiz_answer_events():
    """
    cleanup QuizAnswerEvent

    TODO: how to keep score ?
    """
    pass


def cleanup_quiz_feedback_events():
    """
    cleanup QuizFeedbackEvent

    TODO: 'quiz_feedback_count' field was added, need to update past instances
    """
    pass


class Command(BaseCommand):
    """
    python manage.py cleanup_app_stats
    """

    help = """Group and clean application stats"""

    def handle(self, *args, **kwargs):
        cleanup_question_answer_events()
        cleanup_question_feedback_events()
        # cleanup_quiz_answer_events()
        # cleanup_quiz_feedback_events()


"""
Daily stats
- total number of answers
- total number of answers from questions
- total number of answers from quizs
- total number of quizs played
- total number of feedbacks (like/dislike)
answers per hour ?


Why pandas ?
to do queries in memory instead of querying the database each time
"""
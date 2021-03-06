import time
import yaml
from datetime import datetime

from django.utils import timezone
from django.conf import settings
from django.core.management import BaseCommand

from api import utilities, utilities_stats, utilities_github
from api.models import Configuration


class Command(BaseCommand):
    """
    Usage:
    python manage.py export_data_to_github

    TODO:
    - commit multiple files at once ? https://github.com/PyGithub/PyGithub/issues/1628
    """

    def handle(self, *args, **options):
        # init
        start_time = time.time()

        current_datetime = datetime.now()
        current_datetime_string = current_datetime.strftime("%Y-%m-%d-%H-%M")
        current_datetime_string_pretty = current_datetime.strftime("%Y-%m-%d %H:%M")
        data_update_branch_name = f"data-update-{current_datetime_string}"
        data_update_pull_request_name = (
            f"Data: update ({current_datetime_string_pretty})"
        )

        # update configuration first
        configuration = Configuration.get_solo()
        configuration.github_last_exported = timezone.now()
        configuration.save()

        try:
            # create branch
            utilities_github.create_branch(data_update_branch_name)

            print(
                "--- Step 1 done : init and create branch (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )
            start_time = time.time()

            # update & commit data files
            # data/configuration.yaml
            configuration_yaml = utilities.serialize_model_to_yaml(
                model_label="configuration", flat=True
            )
            utilities_github.update_file(
                file_path="data/configuration.yaml",
                commit_message="update configuration",
                file_content=configuration_yaml,
                branch_name=data_update_branch_name,
            )

            print(
                "--- Step 2.1 done : configuration.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )
            start_time = time.time()

            # data/stats.yaml
            stats_dict = {
                **utilities_stats.question_stats(),
                **utilities_stats.quiz_stats(),
                **utilities_stats.answer_stats(),
                **utilities_stats.category_stats(),
                **utilities_stats.tag_stats(),
                **utilities_stats.contribution_stats(),
            }
            stats_yaml = yaml.safe_dump(stats_dict, allow_unicode=True, sort_keys=False)
            utilities_github.update_file(
                file_path="data/stats.yaml",
                commit_message="update stats",
                file_content=stats_yaml,
                branch_name=data_update_branch_name,
            )

            print(
                "--- Step 2.2 done : stats.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )
            start_time = time.time()

            # data/difficulty-levels.yaml
            difficulty_levels_list = utilities_stats.difficulty_aggregate()
            difficulty_levels_yaml = yaml.safe_dump(
                difficulty_levels_list, allow_unicode=True, sort_keys=False
            )
            utilities_github.update_file(
                file_path="data/difficulty-levels.yaml",
                commit_message="update difficulty levels",
                file_content=difficulty_levels_yaml,
                branch_name=data_update_branch_name,
            )

            print(
                "--- Step 2.3 done : difficulty-levels.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )
            start_time = time.time()

            # data/authors.yaml
            authors_list = utilities_stats.author_aggregate()
            authors_yaml = yaml.safe_dump(
                authors_list, allow_unicode=True, sort_keys=False
            )
            utilities_github.update_file(
                file_path="data/authors.yaml",
                commit_message="update authors",
                file_content=authors_yaml,
                branch_name=data_update_branch_name,
            )

            print(
                "--- Step 2.4 done : authors.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )
            start_time = time.time()

            # data/tags.yaml
            tags_yaml = utilities.serialize_model_to_yaml(model_label="tag", flat=True)
            utilities_github.update_file(
                file_path="data/tags.yaml",
                commit_message="update tags",
                file_content=tags_yaml,
                branch_name=data_update_branch_name,
            )

            print(
                "--- Step 2.5 done : tags.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )
            start_time = time.time()

            # data/questions.yaml
            questions_yaml = utilities.serialize_model_to_yaml(
                model_label="question", flat=True
            )
            utilities_github.update_file(
                file_path="data/questions.yaml",
                commit_message="update questions",
                file_content=questions_yaml,
                branch_name=data_update_branch_name,
            )

            print(
                "--- Step 2.6 done : questions.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )
            start_time = time.time()

            # data/quizzes.yaml
            quizzes_yaml = utilities.serialize_model_to_yaml(
                model_label="quiz", flat=True
            )
            utilities_github.update_file(
                file_path="data/quizzes.yaml",
                commit_message="update quizzes",
                file_content=quizzes_yaml,
                branch_name=data_update_branch_name,
            )

            print(
                "--- Step 2.7 done : quizzes.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )
            start_time = time.time()

            # data/quiz-relationships.yaml
            quiz_relationships_yaml = utilities.serialize_model_to_yaml(
                model_label="quizrelationship", flat=True
            )
            utilities_github.update_file(
                file_path="data/quiz-relationships.yaml",
                commit_message="update quiz relationships",
                file_content=quiz_relationships_yaml,
                branch_name=data_update_branch_name,
            )

            print(
                "--- Step 2.8 done : quiz-relationships.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )
            start_time = time.time()

            # update & commit frontend file
            # frontend/src/constants.js
            old_frontend_constants_file_content = utilities_github.get_file(
                file_path="frontend/src/constants.js",
                branch_name=data_update_branch_name,
            )
            new_frontend_constants_file_content_string = utilities.update_frontend_last_updated_datetime(  # noqa
                old_frontend_constants_file_content.decoded_content.decode(),
                current_datetime_string_pretty,
            )
            utilities_github.update_file(
                file_path="frontend/src/constants.js",
                commit_message="update frontend constants (last_updated datetime)",
                file_content=new_frontend_constants_file_content_string,
                branch_name=data_update_branch_name,
            )

            print(
                "--- Step 2.9 done : constants.js (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )
            start_time = time.time()

            if not settings.DEBUG:
                # create pull request
                pull_request_message = (
                    "Mise à jour de la donnée :"
                    "<ul>"
                    "<li>data/configuration.yaml</li>"
                    "<li>data/stats.yaml</li>"
                    "<li>data/difficulty-levels.yaml</li>"
                    "<li>data/authors.yaml</li>"
                    "<li>data/tags.yaml</li>"
                    "<li>data/questions.yaml</li>"
                    "<li>data/quizzes.yaml</li>"
                    "<li>data/quiz-relationships.yaml</li>"
                    "</ul>"
                )
                pull_request = utilities_github.create_pull_request(
                    pull_request_title=data_update_pull_request_name,
                    pull_request_message=pull_request_message,
                    branch_name=data_update_branch_name,
                    pull_request_labels="automerge",
                )

                print(
                    "--- Step 3 done : created Pull Request (%s seconds) ---"
                    % round(time.time() - start_time, 1)
                )

                # return
                self.stdout.write(pull_request.html_url)
        except Exception as e:
            print(e)
            self.stdout.write(str(e))

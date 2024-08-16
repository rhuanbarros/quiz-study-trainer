import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime

from . import generator_openai
from . import generator_google_gemini


@anvil.server.callable
def generate_questions(title, parameters):
    print("------------------- generate_questions FUNCTION -------------------")

    generator_google_gemini.generate_questions()

    # questionList = generator_openai.chain.invoke(parameters)
    # # questions = json_parser(response)

    # print(questionList.question_itens)

    # for question in questionList.question_itens:
    #     # add to the database
    #     app_tables.questions.add_row(
    #         created_at=datetime.now(),
    #         title=title,
    #         topic_description=question.topic_description,
    #         level=question.level,
    #         question=question.question,
    #         type="true_or_false",
    #         answer_correct=question.answer_correct,
    #         answers=None,
    #         explanation=question.explanation,
    #     )

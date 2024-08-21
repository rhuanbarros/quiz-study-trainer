import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime

from . import generator_openai
from . import generator_google_gemini
from . import generator_groq


@anvil.server.callable
def generate_questions(parameters):
    print("------------------- generate_questions FUNCTION -------------------")

    # generator_google_gemini.generate_questions() #dont work
    # questionList = generator_openai.chain.invoke(parameters) #not free
    questions = generator_groq.generate_questions(parameters)

    print(questions)

    if not isinstance(questions, list):
        questions = [questions]

    for question in questions:
        print(question)
        # add to the database
        app_tables.questions.add_row(
            created_at=datetime.now(),
            title=parameters["title"],
            topic_description=question["topic_description"],
            level=question["level"],
            question=question["question"],
            type="true_or_false",
            answer_correct=question["answer_correct"],
            answers=None,
            explanation=question["explanation"],
            user=anvil.users.get_user(),
        )


@anvil.server.callable
def elaborate_more(question):
    print("elaborate_more server")
    explanation = generator_groq.elaborate_more(question)

    return explanation

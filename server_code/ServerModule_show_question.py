import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime
import uuid

@anvil.server.callable
def get_question():
  question = app_tables.questions.search()[0]
  return question

@anvil.server.callable
def save_answer(answer, question):
  app_tables.answers.add_row(
    created_at=datetime.now(), 
    question=question, 
    got_it_right=answer==bool(question['answer_correct']),
    session=str(uuid.uuid4())
  )
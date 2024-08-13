import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import AIMessage
from typing import List
# import json_repair

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ChatMessage

import json

# from langchain_groq import ChatGroq

# key_google = anvil.secrets.get_secret("GOOGLE_API_KEY")
# llm_google = ChatGoogleGenerativeAI(model="gemini-1.5-flash", convert_system_message_to_human=True, google_api_key=key_google)
# llm_google = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=key_google)

from langchain_core.pydantic_v1 import BaseModel, Field

class Question(BaseModel):
    """ A question about a domain of study."""

    topic_description: str = Field(
        description="A sentence describing the sub-topic to which the question belongs. That means this sentence should specify in a granular level what specific sub-topic the question belongs to. It should be abstract in a way that other questions could be put in this description too. Use between 5 and 10 words."
    )
    level: str = Field(
        description="The difficulty level of the question. It should be only one of the following options: 'easy', 'medium', 'hard'."
    )
    question: str = Field(
        description="The actual question text. It should be a question of type TRUE or FALSE. It means that the questions should be an assertion that could be answered with TRUE or FALSE."
    )
    answer_correct: str = Field(
        description="It should be only one of the following options: TRUE, if the statement of the question is true or FALSE, if the statement of the question is false."
    )
    explanation: str = Field(
        description="An explanation or solution to the question."
    )
    title: str = Field(
        description="An explanation or solution to the question. You should leave this property a empty string."
    )
    type: str = "true_or_false"
    created_at: str = datetime.now()

class QuestionList(BaseModel):
    """A list of Question class."""

    question_itens: list[Question] = Field(
        description="list of Question"
    )

# key_groq = anvil.secrets.get_secret("GROQ_API_KEY")
# llm_groq = ChatGroq(model="llama-3.1-70b-versatile", api_key=key_groq)
# llm_QuestionList = llm_groq.with_structured_output(QuestionList)

object_schema = """{
                    "properties": {
                      "topic_description": {
                        "type": "string",
                        "description": "A sentence describing the sub-topic to which the question belongs. That means this sentence should specify in a granular level what specific sub-topic the question belongs to. It should be abstract in a way that other questions could be put in this description too. Use between 5 and 10 words."
                      },
                      "level": {
                        "type": "string",
                        "description": "The difficulty level of the question. It should be only one of the following options: 'beginner', 'intermediate', 'advanced'."
                      },
                      "question": {
                        "type": "string",
                        "description": "The actual question text. It should be a question of type TRUE or FALSE. It means that the questions should be an assertion that could be answered with TRUE or FALSE."
                      },
                      "answer_correct": {
                        "type": "string",
                        "description": "The correct answer to the question. It should be only one of the following options: TRUE or FALSE"
                      },
                      "explanation": {
                        "type": "string",
                        "description": "An explanation or solution to the question."
                      }
                    },
                    "required": ["topic_description", "level", "question", "answer_correct", "explanation"]
                  }
                  """
prompt_question_generator = PromptTemplate(
  template="""
              TASK CONTEXT:
              I am studying machine learning and I need to practice some questions on various topics.
              
              TASK DESCRIPTION:
              I will provide you with a list of topics, and I would like you to generate a list of TRUE or FALSE questions.
              These questions should be interesting, creative, challenging and thought-provoking. 
              Each question should be in the form of a statement that could be either TRUE or FALSE.
              Feel free to be imaginative and attempt to confuse the student by blending related concepts or similar words.
              I will provide the topics in the DOMAIN KNOWLEDGE section.
              The questions should pertain to these topics, and you can use this knowledge as a foundation to create questions that delve deeper into the subject matter.
              
              ADDITIONAL TASK DESCRIPTION:
              {additional_task_description}
              
              TASK REQUIREMENTS:
              Please refrain from creating questions that require mathematical calculations, but you may create questions with mathematical formulas.
              You SHOULD use LATEX to write mathematical formulas and code, but you should use the Katex flavor.
              Also you should put $$ in the beggining of the katex code and $$ at the end of the code. This is necessary because the interpreter needs it.
              
              TASK DETAILS:
              You should create {quantity} questions of level {level}.
              
              DOMAIN KNOWLEDGE:
              {domain_knowledge}
              
              FORMAT OUTPUT INSTRUCTIONS:
              It should be formatted as described in the output format.
          """,
      input_variables=["quantity", "level", "additional_task_description"],
      partial_variables={"object_schema": object_schema},
  )

# def json_parser(message: AIMessage) -> List[dict]:
#   return json_repair.loads(message.content)

model_name = "gpt-4o-mini"

key_openai = anvil.secrets.get_secret("OPENAI_API_KEY")
llm = ChatOpenAI(model=model_name, api_key=key_openai)
llm_QuestionList = llm.with_structured_output(QuestionList)

# key_google = anvil.secrets.get_secret("GOOGLE_API_KEY")
# llm_google = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=key_google)
# llm_QuestionList = llm_google.with_structured_output(QuestionList)

@anvil.server.callable
def generate_questions(title, parameters):
  print( "------------------- generate_questions FUNCTION -------------------" )

  # response = llm.invoke("Write me a ballad about LangChain")
  # print(response)
  
  # chain = prompt_question_generator | llm_google        
  chain = prompt_question_generator | llm_QuestionList        
  questionList = chain.invoke(parameters)        
  # questions = json_parser(response)

  print(questionList.question_itens)
  
  for question in questionList.question_itens:
    # add to the database
    app_tables.questions.add_row(
      created_at=datetime.now(), 
      title=title, 
      topic_description=question.topic_description, 
      level=question.level,
      question=question.question, 
      type="true_or_false",
      answer_correct=question.answer_correct,
      answers=None,
      explanation=question.explanation
    )


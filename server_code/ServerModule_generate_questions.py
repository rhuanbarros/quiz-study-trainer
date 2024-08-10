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
import json_repair

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

# import nest_asyncio
# nest_asyncio.apply()

key = anvil.secrets.get_secret("GOOGLE_API_KEY")
llm_google = ChatGoogleGenerativeAI(model="gemini-1.5-flash", convert_system_message_to_human=True, google_api_key=key)
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
              The output should be formatted as a JSON list of objects that conforms class object schema below.
              You should output just the Json list. 
              You should not output any other word like "json" in the beginning because it will ruin the parser.

              ```
              {object_schema}
              ```
          """,
      input_variables=["quantity", "level", "additional_task_description"],
      partial_variables={"object_schema": object_schema},
  )

def json_parser(message: AIMessage) -> List[dict]:
  return json_repair.loads(message.content)

@anvil.server.callable
def generate_questions(title, parameters):
  print( "------------------- generate_questions FUNCTION -------------------" )
      
  # try:
  chain = prompt_question_generator | llm_google        
  response = chain.invoke(parameters)        
  questions = json_parser(response)
  
  for question in questions:
    question["title"] = title
    question["type"] = "true_or_false"
    question["created_at"] = datetime.now()
  
    # add to the database
    app_tables.feedback.add_row(**question)
      
  # except Exception as e:
  #     print("An error occurred during the generation:", e)
  

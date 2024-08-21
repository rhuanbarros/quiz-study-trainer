import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from groq import Groq
import json_repair

key_groq = anvil.secrets.get_secret("GROQ_API_KEY")
client = Groq(api_key=key_groq)


json_schema = """
  {
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
  }
"""

prompt_question_generator = """
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
              It should be formatted in list of JSON objects as described below.
              {json_schema}
          """


def generate_questions(parameters):
    prompt_question_generator_formatted = prompt_question_generator.format(
        additional_task_description=parameters["additional_task_description"],
        quantity=parameters["quantity"],
        level=parameters["level"],
        domain_knowledge=parameters["domain_knowledge"],
        json_schema=json_schema,
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt_question_generator_formatted}],
        temperature=1,
        max_tokens=2420,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    completion = response.choices[0].message
    questions = json_repair.loads(completion.content)

    return questions


prompt_elaborate_more = """
                TASK CONTEXT:
                I am studying machine learning practicing some questions.
                
                TASK DESCRIPTION:
                I need you to act like a professor.
                I need you to think critical and answer if the question provided is a TRUE statement or a FALSE.
                You should give a elaborated explanation.
                                
                TASK REQUIREMENTS:
                Use at least 2 sentences to explain your answer.
                
                QUESTION:
                {question}
            """


def elaborate_more(question):
    prompt_elaborate_more_formated = prompt_elaborate_more.format(question=question)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt_elaborate_more_formated}],
        temperature=1,
        max_tokens=2420,
        top_p=1,
        stream=False,
        stop=None,
    )

    completion = response.choices[0].message
    return completion.content

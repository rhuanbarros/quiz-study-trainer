import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This module doesn't work. But some one could use the code to generate questions from its computer and send to the database in other way.
# FailedPrecondition: 400 Gemini API free tier is not available in your country. Please enable billing on your project in Google AI Studio.

# import os
import google.generativeai as genai

key_gemini = anvil.secrets.get_secret("GOOGLE_API_KEY")

genai.configure(api_key=key_gemini)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

llm_gemini = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)


def generate_questions():
    response = llm_gemini.generate_content("Write a story about an AI and magic")
    print(response.text)

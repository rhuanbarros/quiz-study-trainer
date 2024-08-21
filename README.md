# 📚 Machine Learning Interview Preparation Quiz Trainer 

## 🚀 Problem Addressed
I have needed to study some topics in machine learning, but I haven’t found any good specific quizzes about them. 

I have also tried studying with some flashcard apps, but it didn’t work because I had to create the flashcards, and I found it boring because the flashcards didn’t have any kind of provocative appeal, like questions would have. 

Additionally, I want to keep track of the content I study and how many questions I get right and wrong. Therefore, I need a custom UI and fine-grained questions.

## 💡 Solution
I could just ask ChatGPT to create the questions, but it got very repetitive. I realized that if I prompted it with a piece of text about the subject matter, it would create much better questions. So, I created a very customized prompts for this task.

## Frontend (and backend)
- I have used the Anvil framework to create the frontend. Previously, I used Streamlit, but I changed because of the platform's limitations and the difficulty of creating multipage apps. Also, I would like to continue practicing writing Python code, so Anvil seems to be a good option.
- There is a feature that, when I don't know the answer, I can click a button, and it automatically queries the LLM model to explain the topic for me. This way, I don't need to leave the app and can continue the study session seamlessly.
- I also wanted to keep track of my results over time, so there is a page to show a study report.

## Community development
I created this project to enable development with anyone who needs a similar solution. Therefore, we can create new features quickly. All pull requests are welcome.

[Take a look at this page to know how to open this project using Anvil Cloud.](ANVIL_README.MD)


## Online version hosted
You can access a free online version of this app hosted on Anvil Cloud at https://ill-informed-careless-panther.anvil.app/


## Key Points
- 🐍 **Python**: Completely coded in Python using the Anvil framework (frontend and backend).
- 🧠 **Prompt engeneering**: Customized prompt for better question creation.
- 📈 **Enhanced Learning**: Improves memorization of concepts similiar to Spaced Repetion techinique.
- 📚 **Integrated Knowledge**: Query LLM model directly for explanations without leaving the app.
- 🗂️ **Result Tracking**: Keep track of study progress and quiz results over time.
- ☁️ **Cloud Accessibility**: Hosted in the cloud for access on mobile devices.


## TODO
- Study report
  - show how the progress is for each subject matter studied (I need to define this better)
  - plot some graphs of evolution
  - show questions that I already have memorized
  - show quentions that I keep get it wrong

- Show question
  - Create a ranking algorithm to sort the questions already answered to allow some kind of space repetition memorization.


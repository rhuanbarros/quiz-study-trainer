import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import pand


@anvil.server.callable
def get_df_by_topic():
    answers = app_tables.answers.search()

    answers_list = [
        {
            "created_at": r["created_at"],
            "question_question": r["question"]["question"],
            "question_title": r["question"]["title"],
            "question_type": r["question"]["type"],
            "question_level": r["question"]["level"],
            "got_it_right": r["got_it_right"],
            "session": r["session"],
            "user": r["user"]["email"],
        }
        for r in answers
    ]

    df = pd.DataFrame.from_dict(answers_list)

    df_by_topic = (
        df.groupby(["question_title"])["got_it_right"]
        .value_counts()
        .unstack(fill_value=0)
    )
    df_by_topic = df_by_topic.rename(columns={False: "Wrong", True: "Right"})
    df_by_topic = df_by_topic.sort_values(by="Wrong", ascending=False)

    return df_by_topic.to_markdown()

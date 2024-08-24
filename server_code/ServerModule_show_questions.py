import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import pandas as pd


@anvil.server.callable
def get_question_revision(self):
    answers = app_tables.answers.search()

    answers_list = [
        {
            "created_at": r["created_at"],
            "question_data": r["question"],
            "question": r["question"]["question"],
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

    df_wrong = (
        df.groupby(["question"])["got_it_right"].value_counts().unstack(fill_value=0)
    )
    df_wrong = df_wrong.rename(columns={False: "Wrong", True: "Right"})
    df_wrong = (
        df_wrong.reset_index()
    )  # Reset index to move 'question_question' into a column
    df_wrong = df_wrong.sort_values(by="Wrong", ascending=False)
    df_wrong = df_wrong[["question", "Wrong", "Right"]]  # Select the desired columns
    df_wrong = df_wrong.reset_index(drop=True)
    df_wrong.columns.name = None

    df_wrong["Wrong_percent"] = df_wrong["Wrong"] / (
        df_wrong["Wrong"] + df_wrong["Right"]
    )
    df_wrong["wrong_normalized"] = df_wrong["Wrong"] / df_wrong["Wrong"].sum()
    df_wrong = df_wrong.set_index("question")

    # from datetime import datetime
    # import pytz

    # Assuming 'created_at' is in UTC, convert datetime.now() to UTC
    # now_aware = datetime.now(pytz.UTC)
    now_aware = datetime.now()

    df_created = df.groupby(["question"])["created_at"].max().reset_index()
    df_created = df_created.set_index("question")
    df_created["time_diff_from_now"] = now_aware - df_created["created_at"]
    # df_created["time_diff_from_now"] = df_created["time_diff_from_now"].apply( lambda x: int( x.total_seconds() / 60 ) )
    df_created["time_diff_from_now"] = df_created["time_diff_from_now"].apply(
        lambda x: int(x.total_seconds())
    )
    df_created = df_created.drop(columns="created_at")
    df_created["time_diff_from_now_normalized"] = (
        df_created["time_diff_from_now"] / df_created["time_diff_from_now"].sum()
    )

    df_answer_stats = df_wrong.join(df_created)

    def score(row):
        weights = {"wrong_normalized": 1, "time_diff_from_now_normalized": 1}

        return (
            row["wrong_normalized"] * weights["wrong_normalized"]
            + row["time_diff_from_now_normalized"]
            * weights["time_diff_from_now_normalized"]
        )

    df_score = (
        df_answer_stats.apply(score, axis=1).sort_values(ascending=False).reset_index()
    )
    df_score = df_score.set_index("question")
    df_score.columns = ["score"]

    df_data = df[["question_data", "question"]]
    df_data = df_data.set_index("question")

    df_score_ = df_score.join(df_data)

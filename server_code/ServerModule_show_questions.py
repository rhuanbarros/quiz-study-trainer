import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import pandas as pd
from datetime import datetime
import pytz


@anvil.server.callable
def get_question_revision():
    print("get_question_revision")

    answers = app_tables.answers.search()

    answers_list = [
        {
            "created_at": r["created_at"],
            "question_data": r["question"],
            "question_txt": r["question"]["question"],
            "question_title": r["question"]["title"],
            "question_type": r["question"]["type"],
            "question_level": r["question"]["level"],
            "got_it_right": r["got_it_right"],
            "session": r["session"],
            "user": r["user"]["email"] if r["user"] else "",
        }
        for r in answers
    ]

    aq = {}
    total_wrong = 0
    total_right = 0

    for ans in answers_list:
        key = ans["question_txt"]
        got_it_right = ans["got_it_right"]

        if key not in aq:
            aq[key] = {
                "question_data": ans["question_data"],
                "last_answered": ans["created_at"],
                "wrong": 0,
                "right": 1,
            }

        aq[key]["last_answered"] = max(ans["created_at"], aq[key]["last_answered"])

        if got_it_right:
            aq[key]["right"] += 1
            total_wrong += 1
        else:
            aq[key]["wrong"] += 1
            total_right += 1

    now_aware = datetime.now(pytz.UTC)
    total_time = 0
    for key in aq:
        aq[key]["wrong_normalized"] = aq[key]["wrong"] / total_wrong
        aq[key]["right_normalized"] = aq[key]["right"] / total_right
        aq[key]["time_diff"] = int(
            (now_aware - aq[key]["last_answered"]).total_seconds()
        )
        total_time += aq[key]["time_diff"]

    for key in aq:
        aq[key]["time_diff"] = aq[key]["time_diff"] / total_time

    def score(row):
        weights = {"wrong_normalized": 1, "time_diff": 1}

        return (
            row["wrong_normalized"] * weights["wrong_normalized"]
            + row["time_diff"] * weights["time_diff"]
        )

    for key in aq:
        aq[key]["score"] = score(aq[key])

    aq_list = [(v["question_data"], v["score"]) for k, v in aq.items()]

    questions_ranking = sorted(aq_list, key=lambda row: row[1], reverse=False)
    questions_ranking_ = [e[0] for e in questions_ranking]

    return questions_ranking_

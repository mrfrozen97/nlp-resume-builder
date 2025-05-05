# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import os

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.exceptions import FileIOException

import requests
from pypdf import PdfReader

import config


def update(
    dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
) -> List[Dict[Text, Any]]:
    try:
        response = requests.post(
            f"{config.API_STATE_URL}?sender_id={tracker.sender_id}",
            json=tracker.current_state(),
        )
        response.raise_for_status()
    except requests.exceptions.BaseHTTPError as e:
        raise FileIOException(str(e)) from e


class ActionOptimizeResume(Action):

    def name(self) -> Text:
        return "action_optimize_resume"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        result = []
        optimized_resume = tracker.get_slot("optimized_resume")
        if not optimized_resume:
            dispatcher.utter_message(text="I am optimizing your resume now...")
            try:
                reader = PdfReader(
                    os.path.join(os.path.dirname(__file__), "../file/user1.pdf")
                )
                text = "\n".join([page.extract_text() for page in reader.pages])
                with open(
                    os.path.join(os.path.dirname(__file__), "../file/jd.txt")
                ) as f:
                    job_description = f.read()
                response = requests.post(
                    f"{config.API_OPTIMIZE_URL}",
                    json={"resume_text": text, "job_description": job_description},
                )
                response.raise_for_status()
                optimized_resume = response.text
                result.append(SlotSet("optimized_resume", optimized_resume))
                tracker.slots["optimized_resume"] = optimized_resume
                # update(dispatcher, tracker, domain)
                dispatcher.utter_message(text=f"{optimized_resume}")
            except requests.exceptions.BaseHTTPError as e:
                raise FileIOException(str(e)) from e
        else:
            dispatcher.utter_message(text=f"{optimized_resume}")
        return result


class ActionScore(Action):

    def name(self) -> Text:
        return "action_score"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        score = tracker.get_slot("score")
        if not score:
            dispatcher.utter_message(text="I am computing your score now...")
            try:
                reader = PdfReader(
                    os.path.join(os.path.dirname(__file__), "../file/user1.pdf")
                )
                text = "\n".join([page.extract_text() for page in reader.pages])
                with open(
                    os.path.join(os.path.dirname(__file__), "../file/jd.txt")
                ) as f:
                    job_description = f.read()
                response = requests.post(
                    f"{config.API_SCORE_URL}",
                    json={"resume_text": text, "job_description": job_description},
                )
                response.raise_for_status()
                score = response.json()["normalized_score"]
                result = SlotSet("score", score)
                tracker.slots["score"] = score
                update(dispatcher, tracker, domain)
                dispatcher.utter_message(text=f"Your score is {score}")
            except requests.exceptions.BaseHTTPError as e:
                raise FileIOException(str(e)) from e
        else:
            dispatcher.utter_message(text=f"Your score is {score}")
        return [result]


class ActionCompany(Action):

    def name(self) -> Text:
        return "action_company"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        company = tracker.get_slot("company")
        if not company:
            dispatcher.utter_message(text="I don't know your company.")
        else:
            dispatcher.utter_message(text=f"Your company is {company}")

        update(dispatcher, tracker, domain)
        return []


class ActionSkill(Action):

    def name(self) -> Text:
        return "action_skill"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        skill = tracker.get_slot("skill")
        if not skill:
            dispatcher.utter_message(text="I don't know your skills.")
        else:
            dispatcher.utter_message(text=f"Your skill set is {skill}")

        update(dispatcher, tracker, domain)
        return []


class ActionJobTitle(Action):

    def name(self) -> Text:
        return "action_job_title"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        job_title = tracker.get_slot("job_title")
        if not job_title:
            dispatcher.utter_message(text="I don't know your job title.")
        else:
            dispatcher.utter_message(text=f"Your job title is {job_title}")

        update(dispatcher, tracker, domain)
        return []


# class ActionJobDescription(Action):
#
#     def name(self) -> Text:
#         return "action_job_description"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         job_description = tracker.get_slot("job_description")
#         if not job_description:
#             dispatcher.utter_message(text="I don't know your job description.")
#         else:
#             dispatcher.utter_message(text=f"Your job title is {job_description}")
#
#         update(dispatcher, tracker, domain)
#         return []

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


def update(dispatcher: CollectingDispatcher, tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    try:
        response = requests.post(f"{config.API_STATE_URL}?sender_id={tracker.sender_id}", json=tracker.current_state())
        response.raise_for_status()
    except requests.exceptions.BaseHTTPError as e:
        raise FileIOException(str(e)) from e


class ActionScoreResume(Action):
    def name(self) -> Text:
        return "action_score_resume"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        score_resume = tracker.get_slot("score_resume")
        result = []
        if not score_resume:
            dispatcher.utter_message(text="I am computing your resume score now...")
            try:
                reader = PdfReader(os.path.join(os.path.dirname(__file__), "../file/user1.pdf"))
                text = "\n".join([page.extract_text() for page in reader.pages])
                with open(
                    os.path.join(os.path.dirname(__file__), "../file/jd.txt")
                ) as f:
                    job_description = f.read()
                response = requests.post(f"{config.API_SCORE_RESUME_URL}", json={"resume_text": text, "job_description": job_description})
                response.raise_for_status()
                score_resume = response.json()["normalized_score"]
                result.append(SlotSet("score_resume", score_resume))
                tracker.slots["score_resume"] = score_resume
                update(dispatcher, tracker, domain)
                dispatcher.utter_message(text=f"Your resume score is {score_resume}")
            except requests.exceptions.BaseHTTPError as e:
                raise FileIOException(str(e)) from e
        else:
            dispatcher.utter_message(text=f"Your resume score is {score_resume}")
        return result


class ActionScoreImpact(Action):
    def name(self) -> Text:
        return "action_score_impact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        score_impact = tracker.get_slot("score_impact")
        result = []
        if not score_impact:
            dispatcher.utter_message(text="I am computing your score impact now...")
            try:
                reader = PdfReader(os.path.join(os.path.dirname(__file__), "../file/user1.pdf"))
                text = "\n".join([page.extract_text() for page in reader.pages])
                response = requests.post(f"{config.API_SCORE_IMPACT_URL}", json={"resume_text": text})
                response.raise_for_status()
                score_impact = response.json()["score"]
                result.append(SlotSet("score_impact", score_impact))
                tracker.slots["score_impact"] = score_impact
                update(dispatcher, tracker, domain)
                dispatcher.utter_message(text=f"Your score impact is {score_impact}")
            except requests.exceptions.BaseHTTPError as e:
                raise FileIOException(str(e)) from e
        else:
            dispatcher.utter_message(text=f"Your score impact is {score_impact}")
        return result


class ActionCompany(Action):
    def name(self) -> Text:
        return "action_company"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        job_title = tracker.get_slot("job_title")
        if not job_title:
            dispatcher.utter_message(text="I don't know your job title.")
        else:
            dispatcher.utter_message(text=f"Your job title is {job_title}")

        update(dispatcher, tracker, domain)
        return []


class ActionJobDescription(Action):
    def name(self) -> Text:
        return "action_job_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        job_description = tracker.get_slot("job_description")
        if not job_description:
            dispatcher.utter_message(text="I don't know your job description.")
        else:
            dispatcher.utter_message(text=f"Your job title is {job_description}")

        update(dispatcher, tracker, domain)
        return []

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.exceptions import FileIOException

import requests

import config


def update(dispatcher: CollectingDispatcher, tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    try:
        response = requests.post(f"{config.API_STATE_URL}?sender_id={tracker.sender_id}", json=tracker.current_state())
        response.raise_for_status()
    except requests.exceptions.BaseHTTPError as e:
        raise FileIOException(str(e)) from e


class ActionScore(Action):

    def name(self) -> Text:
        return "action_score"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # score = tracker.get_slot("score")
        # if not company:
        #     dispatcher.utter_message(text="I don't know your company.")
        # else:
        #     dispatcher.utter_message(text=f"Your company is {company}")

        try:
            response = requests.post(f"{config.API_SCORE_URL}", json={"resume_text": "string", "job_description": "string"})
            response.raise_for_status()
        except requests.exceptions.BaseHTTPError as e:
            raise FileIOException(str(e)) from e
        tracker.slots["score"] = response.json()["normalized_score"]
        update(dispatcher, tracker, domain)
        return []


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

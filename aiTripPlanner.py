from enum import Enum
from datetime import datetime
from openAiUtils import GptUtils, GptType

from fastapi import FastAPI, Request
from typing import List, Dict


app = FastAPI()


@app.post("/process/")
async def process_endpoint(request: Request):
    input_json = await request.json()
    print("Received json:", input_json)
    result = process(input_json)


def process(input_json: Dict):
    # Data exists
    if ("trip_type" not in input_json or "budget" not in input_json or
            "from_date" not in input_json or "to_date" not in input_json):
        return {}

    trip_type = input_json["trip_type"]
    from_date = input_json["from_date"]
    to_date = input_json["to_date"]

    # Validate data
    if trip_type not in ["Beach", "Ski", "City"]:
        return {}

    try:
        # Attempt to parse the string as a date
        datetime.strptime(from_date, "%d/%m")
        datetime.strptime(to_date, "%d/%m")
    except ValueError:
        return {}

    budget = input_json["budget"]
    if not budget.isdigit():
        return {}
    budget = int(budget)

    # Now start the real process

    gpt_utils = GptUtils()
    cities_prompt = f"{from_date}/{to_date}, {trip_type}"
    cities = gpt_utils.ask_gpt_for_help(GptType.CITY_ADVISOR, cities_prompt)
    res = gpt_utils.ask_gpt_for_help(GptType.DAILY_TRIP_PLANNER, "22/3-25/3, Phuket, Thailand")
import json
from datetime import datetime

from serpapiUtils import SerpapiUtils
from openAiUtils import GptUtils, GptType

from fastapi import FastAPI, Request
from typing import List, Dict


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process_data/")
async def process_endpoint(request: Request):
    input_json = await request.json()
    print("Received json:", input_json)
    result = process(input_json)
    return result


def process(input_json: Dict):
    # Data exists
    if ("trip_type" not in input_json or "budget" not in input_json or
            "from_date" not in input_json or "to_date" not in input_json):
        return {}

    trip_type = str(input_json["trip_type"]).capitalize()
    from_date = input_json["from_date"]
    to_date = input_json["to_date"]

    # Validate data
    if trip_type not in ["Beach", "Ski", "City"]:
        return {}

    try:
        # Attempt to parse the string as a date
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
    except ValueError:
        return {}

    budget = input_json["budget"]
    if not budget.isdigit():
        return {}
    budget = int(budget)

    # Now start the real process

    gpt_utils = GptUtils()
    serpapi_utils = SerpapiUtils(from_date, to_date)

    from_month_and_day_only = from_date.strftime('%d/%m')
    to_month_and_day_only = to_date.strftime('%d/%m')

    cities_prompt = f"{from_month_and_day_only}/{to_month_and_day_only}, {trip_type}"
    # cities = gpt_utils.ask_gpt_for_help(GptType.CITY_ADVISOR, cities_prompt)
    # res = gpt_utils.ask_gpt_for_help(GptType.DAILY_TRIP_PLANNER, "22/3-25/3, Phuket, Thailand")
    return serpapi_utils.plan_trip_hotel_flight([{"Place": "Phuket, Thailand", "Airport_code": "HKT"}], 800)




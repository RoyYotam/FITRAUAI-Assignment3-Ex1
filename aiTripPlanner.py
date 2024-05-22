from datetime import datetime

from starlette.responses import FileResponse

from serpapiUtils import SerpapiUtils
from openAiUtils import GptUtils, GptType

from fastapi import FastAPI, Request
from typing import Dict


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
    try:
        input_json = await request.json()
        print("Received json:", input_json)
        return process(input_json)
    except Exception as _:
        return {}


@app.post("/daily_plan/")
async def daily_plan_endpoint(request: Request):
    try:
        input_json = await request.json()
        print("Received json:", input_json)
        return daily_plan(input_json)
    except Exception as _:
        return {}


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
    cities = gpt_utils.ask_gpt_for_help(GptType.CITY_ADVISOR, cities_prompt)

    if 'Locations' not in cities:
        return {}

    return serpapi_utils.plan_trip_hotel_flight(cities['Locations'], budget)


def daily_plan(input_json: Dict):
    # Data exists
    if ("location" not in input_json or
            "from_date" not in input_json or "to_date" not in input_json):
        return {}

    location = input_json["location"]
    from_date = input_json["from_date"]
    to_date = input_json["to_date"]

    # Validate data
    try:
        # Attempt to parse the string as a date
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
    except ValueError:
        return {}

    # Now start the real process
    gpt_utils = GptUtils()

    from_month_and_day_only = from_date.strftime('%d/%m')
    to_month_and_day_only = to_date.strftime('%d/%m')

    daily_plan_prompt = f"{from_month_and_day_only}/{to_month_and_day_only}, {location}"
    res = gpt_utils.ask_gpt_for_help(GptType.DAILY_TRIP_PLANNER, daily_plan_prompt)

    if 'Prompt' in res:
        images_paths = gpt_utils.ask_gpt_for_images(res["Prompt"])
        res["images_paths"] = images_paths

    return res


@app.get("/images/{image_name}")
async def get_image(image_name: str):
    # Note, this implementation do not validate image_path (to prevent directory traversal attacks).
    image_path = f"./images/{image_name}"
    return FileResponse(image_path)




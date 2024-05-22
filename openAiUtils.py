from enum import Enum
from openai import OpenAI
import json
import base64
from datetime import datetime
import os


class GptType(Enum):
    CITY_ADVISOR = 1
    DAILY_TRIP_PLANNER = 2


class GptUtils:
    def __init__(self):
        self.my_key = "MY_KEY_HERE"
        self.client = OpenAI(api_key=self.my_key)
        self.get_day_trip_by_city_and_trip_time_message = \
            {"role": "system", "content":
                """
                You are trip planner master! No one can plan better trip than you are. 
                When a user tell you the when(dd/mm-dd/mm) and where(city), you will plan a daily trip for every date between those dates.
                In addition, you will provide exactly 4 different prompts to write to dall-e, they will create a picture of some trip activities.
                The result should be in a Json only -  
                { "DayTripInfo": [ 
                { 
                "Date" : "dd/mm",   
                "Activities":  [{"TimeOnDay":  hour:minutes,  "Activity": ""}, ...]   
                } ]
                , "Prompt": [""]
                }
                """}
        self.get_cities_by_time_and_trip_type_message = \
            {"role": "system", "content":
                """
                You are trip master! You've been in every country in the world, and you can provide the best match for a trip.
                You receive time of trip (dd/mm-dd/mm), and trip type, and return 5 possible places in the world to travel.
                The result should be in json:
                {
                "Locations": [{"Place": "", "AirportCode: ""}, ...]              
                }"
                """}

    def ask_gpt_for_help(self, gpt_type: GptType, user_input: str) -> {}:
        system_message = self.get_cities_by_time_and_trip_type_message if gpt_type is GptType.CITY_ADVISOR \
            else self.get_day_trip_by_city_and_trip_time_message

        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                max_tokens=6000,
                messages=[
                    system_message,
                    {"role": "user", "content": user_input}
                ]
            )

            return json.loads(completion.choices[0].message.content)
        except Exception as _:
            return None

    def ask_gpt_for_images(self, dalle_inputs: [str]) -> []:
        files_names = self.generate_unique_img_name(num_of_files=4)
        available_images = []

        for dalle_input, file_name in zip(dalle_inputs, files_names):
            try:
                img_data = self.dalle_single_image_creator(dalle_input)
                image_data_base64 = img_data.b64_json
                image_data = base64.b64decode(image_data_base64)

                self.validate_images_directory(file_name)
                with open(file_name, "wb") as fh:
                    fh.write(image_data)

                    available_images.append(file_name)

            except Exception as _:
                continue

        return available_images

    def dalle_single_image_creator(self, dalle_input: str):
        response = self.client.images.generate(
            model="dall-e-2",
            prompt=dalle_input,
            size="1024x1024",
            response_format="b64_json",
            n=1,
        )

        return response.data[0]

    @staticmethod
    def generate_unique_img_name(num_of_files=1) -> []:
        unique_name_list = []

        extension = 'png'
        images_directory = 'images'
        current_time = datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d__%H-%M')  # Format: YYYYMMDDHHMMSS

        for i in range(num_of_files):
            unique_name = f"{images_directory}/img_{i + 1}__{timestamp}.{extension}"
            unique_name_list.append(unique_name)

        return unique_name_list

    @staticmethod
    def validate_images_directory(file_path: str):
        # Extract directory path from file path
        directory = os.path.dirname(file_path)

        # Check if directory exists, if not, create it
        if not os.path.exists(directory):
            os.makedirs(directory)


if __name__ == "__main__":
    gptUtils = GptUtils()
    # res = gptUtils.ask_gpt_for_help(GptType.CITY_ADVISOR, "22/3-25/3, Beach")
    # res = gptUtils.ask_gpt_for_help(GptType.DAILY_TRIP_PLANNER, "22/3-25/3, Phuket, Thailand")
    # test_message = """
    #                     Generate an image of colorful buildings and street art in Old Phuket Town
    #                     """
    # print(gptUtils.ask_gpt_for_images([test_message]))


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
                When a user tell you the when(dd/mm-dd/mm) and where(city), you will plan a daily trip for for every day of his vacation.
                In addition, you will provide a prompt to write to dall-e to create a picture of the trip.
                The result should be in a Json only -  
                { "Day_trip_info":  
                { 
                "Date" : "dd/mm",   
                "Activities":  [{"TIME_ON_DAY":  hour:minutes,  "Activity": ""}, ...]   
                }
                , "Prompt": ""
                }
                """}
        self.get_cities_by_time_and_trip_type_message = \
            {"role": "system", "content":
                """
                You are trip master! You've been in every country in the world, and you can provide the best match for a trip.
                You receive time of trip (dd/mm-dd/mm), and trip type, and return 5 possible places in the world to travel.
                The result should be in json:
                {
                "Locations": [{"Place": "", "Airport_code: ""}, ...]              
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

    def ask_gpt_for_image(self, dalle_input: str) -> []:
        try:
            response = self.client.images.generate(
                model="dall-e-2",
                prompt=dalle_input,
                size="1024x1024",
                response_format="b64_json",
                n=4,
            )

            images = response.data
            files_names = self.generate_unique_img_name(num_of_files=4)

            for file_name, img_data in zip(files_names, images):
                image_data_base64 = img_data.b64_json
                image_data = base64.b64decode(image_data_base64)

                self.validate_images_directory(file_name)
                with open(file_name, "wb") as fh:
                    fh.write(image_data)

            return files_names

        except Exception as _:
            return None

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
    test_message = """
                        Create a picture of the beautiful beaches and vibrant culture of Phuket, Thailand. Show the Big Buddha, Patong Beach, Phi Phi Islands, Similan Islands, and the stunning sunset at Promthep Cape.
                        """
    print(gptUtils.ask_gpt_for_image(test_message))


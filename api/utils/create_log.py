from datetime import datetime
import os

def create_log(message):
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    file_path = f"api/logs/{year}/{month}/{day}/logs.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a") as file:
        message = f"{str(datetime.now())} - {message}"
        formated_message = f'{message}\n'
        file.write(formated_message)

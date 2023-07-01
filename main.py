from twilio.rest import Client
import data_manager
from UI import UserInterface

TWILIO_ACC_SID = "####SID####"
AUTH_TOKEN = "####AUTH_TOKEN####"

manager = data_manager.DataManager()
ui = UserInterface()
client = Client(TWILIO_ACC_SID, AUTH_TOKEN)
from_number = "+19897188875"
i = 0

while i >= 0:
    try:
        data = manager.get_data(i)
        price = data["price"]
        from_loc = data["from"]
        to_loc = data["to"]
        to_number = data["number"]
        to_number_f = f"+91{to_number}"
        depart_date = data["date"]
        depart_time = data["time"]
        link = data["link"]
        i = i + 1
        message_body = f"CONGRATS, we found a deal for you, there is a flight from {from_loc} to {to_loc} with a lowest fare of Rs {price},\nDEPARTURE DATE: {depart_date}\nDEPARTURE TIME: {depart_time}\nClick link to book: {link}"
        message = client.messages \
            .create(
                body=message_body,
                from_=from_number,
                to=to_number_f
            )
        print(message.status)
        print(message_body)
    except (IndexError, TypeError) as e:
        i = -1
        break

import chainlit as cl
from agents import function_tool
import requests
import os

@function_tool
def send_whatsapp_message(number:str,message:str)->str:
    """uses the ultra msg api to send a custom whatsapp message to the
    specified phone number.return a success message if sent seccessfully.or an error
    message if the request fails"""

    instance_id=os.getenv("instance_id")
    token=os.getenv("API_TOKEN")
    url=f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload={
        "token":token,
        "to":number,
        "body":message
    }
    response=requests.post(url,data=payload)
    if response.status_code==200:
        return f"==message  sent successfully to{number}"
    else:
        return f"failed to send message:error:{response.text}"
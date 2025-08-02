from agents import Agent,Runner,OpenAIChatCompletionsModel,set_tracing_disabled,function_tool
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
from whatsapp import send_whatsapp_message
import asyncio
import chainlit as cl

load_dotenv()

set_tracing_disabled(True)

OPENAI_API_KEY=os.getenv("OPEN_API_KEY")

external_client=AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model=OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)
@function_tool
def get_user_data(min_age:int)->list[dict]:
    "retrive user data on a minimum age"
    users = [
    { "name": "ali", "age": 20, "gender": "male", "education": "Intermediate", "hobbies": ["cricket", "reading"] },
    { "name": "rehman", "age": 25, "gender": "male", "education": "BBA", "hobbies": ["football", "coding"] },
    { "name": "ahmed", "age": 30, "gender": "male", "education": "MBA", "hobbies": ["traveling", "photography"] },
    { "name": "usman", "age": 22, "gender": "male", "education": "BS Computer Science", "hobbies": ["gaming", "swimming"] },
    { "name": "zain", "age": 27, "gender": "male", "education": "MSc", "hobbies": ["music", "cycling"] },
    { "name": "farhan", "age": 24, "gender": "male", "education": "B.Com", "hobbies": ["cricket", "blogging"] },
    { "name": "hassan", "age": 28, "gender": "male", "education": "Electrical Engineering", "hobbies": ["tech reviews", "chess"] },
    { "name": "salman", "age": 26, "gender": "male", "education": "Mechanical Engineering", "hobbies": ["football", "poetry"] },
    { "name": "danish", "age": 23, "gender": "male", "education": "BBA", "hobbies": ["gaming", "social media"] },
    { "name": "junaid", "age": 29, "gender": "male", "education": "MCS", "hobbies": ["reading", "gym"] },
    { "name": "hamza", "age": 21, "gender": "male", "education": "BS Software Engineering", "hobbies": ["coding", "e-sports"] },
    { "name": "saad", "age": 31, "gender": "male", "education": "MBA", "hobbies": ["public speaking", "running"] },
    { "name": "bilal", "age": 33, "gender": "male", "education": "PhD Economics", "hobbies": ["writing", "cooking"] },
    { "name": "waleed", "age": 32, "gender": "male", "education": "MPhil", "hobbies": ["movies", "traveling"] },
    { "name": "ibrahim", "age": 35, "gender": "male", "education": "BS Physics", "hobbies": ["gardening", "DIY crafts"] },
    { "name": "yasir", "age": 36, "gender": "male", "education": "CA", "hobbies": ["finance blogs", "board games"] },
    { "name": "talha", "age": 34, "gender": "male", "education": "LLB", "hobbies": ["debates", "documentaries"] },
    { "name": "fahad", "age": 38, "gender": "male", "education": "M.Ed", "hobbies": ["mentoring", "history books"] },

    # Female Users (Girls)
    { "name": "ayesha", "age": 23, "gender": "female", "education": "BS Psychology", "hobbies": ["painting", "baking"] },
    { "name": "fatima", "age": 25, "gender": "female", "education": "MSc Zoology", "hobbies": ["gardening", "reading"] },
    { "name": "noor", "age": 22, "gender": "female", "education": "BBA", "hobbies": ["vlogging", "fashion design"] },
    { "name": "hira", "age": 27, "gender": "female", "education": "MBBS", "hobbies": ["photography", "poetry"] },
    { "name": "bareera", "age": 21, "gender": "female", "education": "BS IT", "hobbies": ["coding", "writing stories"] }
]


    
    for user in users:
        if user["age"]<min_age:
            user.remove(user)
        return users
    
match_agent=Agent(
        name="perfect match",
        instructions=""" you are a rishta finder find a perfect match from a custom tool based on age only.reply short and sed whatsapp message only if user asks""",
        model=model,
        tools=[get_user_data,send_whatsapp_message]

)

@cl.on_chat_start
async def start():
    cl.user_session.set("history",[])
    await cl.Message("Hi!, i am as doing my best to find a a perfect life partner to you.tell me your name ,age,gender and whatsapp number").send()
@cl.on_message
async def main(message: cl.Message):
    await cl.Message("Thinking...").send()
    history = cl.user_session.get("history") or []
    history.append({"role": "user", "content": message.content})

    result = await Runner.run(  
        starting_agent=match_agent,
        input=history
    )
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()
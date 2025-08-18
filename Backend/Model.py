import cohere
from rich import print 
from dotenv import dotenv_values

#load enviroment variabl from the .env file 
env_vars = dotenv_values(".env")

#API Key 
cohereAPIKey = env_vars.get("cohereAPIKey")


co = cohere.Client(api_key=cohereAPIKey)

#define the recognize function to perform task 
funcs = [
    "exit","general","realtime","open", "close", "play",
    "generate image", "system" , "content" , " google search ",
    "youtube search " , "reminder"
]

messages =[]

preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond 


ChatHistory = [
    {"role" : "User","message": "how are you?"},
    {"role" : "Chatbot","message": " general how are you?"},
    {"role" : "User","message": "do you like pizza? "},
    {"role" : "Chatbot","message": "general do you like pizza?"},
    {"role" : "User","message": "open chrome and tell me about Quaid e Azam."},
    {"role" : "Chatbot","message": "open chrome, general and tell me about Quaid e Azam."},
    {"role" : "User","message": "open chrome and firefox"},
    {"role" : "Chatbot","message": "open chrome , open firefox"},
    {"role" : "User","message": "what is today's date and by the way renind me that i have a dancing performence on 5th aug at 11pm"},
    {"role" : "Chatbot","message": " general what is today's date , reminder 11:00 pm 5th aug dancing performence"},
    {"role" : "User","message": "chat with me "},
    {"role" : "User","message": " general chat with me "},
]

def FirstLayerDMM(prompt: str = "test"):
    
    messages.append({"role": "user", "content" : f"{prompt}"})
    
    stream = co.chat_stream(
        model='command-r-plus',
        message=prompt,
        temperature=0.7,
        chat_history=ChatHistory,
        prompt_truncation='OFF',
        connectors=[],
        preamble=preamble    
        )
    
    response = ""
    
    for event in stream:
        if event.event_type == "text_generation":
            response += event.text
            

response = response.replace("\n", "")
response = response.split(",")

response = [i.strip() for i in response]

temp = []

for task in response :
     for func in funcs:
         if task.startswith(func):
             temp.append(task)
             
response = temp
    
if '(query)' in response:
    newresponse = FirstLayerDMM(prompt=prompt)
    return newresponse
else:
    return response

if __name__ == "__main__":
    while True:
        print(FirstLayerDMM(input(">>> ")))
    
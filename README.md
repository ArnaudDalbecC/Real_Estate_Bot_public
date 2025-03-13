This project aims to automate the early stage interactions between a potential client
and a real estate agent. To achieve this, I use a pre-trained LLM and feed it with a 
context window and the conversation with the client. The bot automatically responds to the
emails it receives.

To execute the program, run usage.py

You should write to the bot first so that it responds to your email when you execute the program

IMPORTANT:
When creating a new email account for the bot, use the app password (16 digits that can be found in the gmail settings)

TODO:
 - separate context from chat.py file
 - add possibility to add a pdf file for context
 - find prompt size boundary for Mistral-7B-Instruct-v0.1
 - deploy on cloud

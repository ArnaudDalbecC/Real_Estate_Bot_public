from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class chatbot():
    
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        # Log in (only needed if downloading the model programmatically)
        self.token = "insert_token_here" # Get token from hugginface website for the corresponding model

        # Load the model and tokenizer
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.1" # Use any other models
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=self.token)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, torch_dtype=torch.float16, device_map="auto", token=self.token)

    # Chat function
    def chat(self, system_context, conversation_history, user_message):
        # Format for Mistral-Instruct
        prompt = f"<s>[INST] \nSystem: {system_context}\n\n"
        
        if conversation_history:
            prompt += f"Previous conversation:\n{conversation_history}\n\n"
        
        prompt += f"Client: {user_message}\n[/INST]"
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
        outputs = self.model.generate(**inputs, max_new_tokens=1000)
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the input prompt from the response
        response = response.replace(prompt, "").strip()
        return response

    # Example chat
    def main(self, customer_message):
        # Describe the bot's behavior (give all the information it needs about the property or anything else)
        bot_context = "I want you to interact with the user as if you were a real estate agent"
        discussion = ''
        
        
        #customer_message = input("Enter your message here: ")

        # Create the full prompt with context and pass it to chat
            
        bot_message = self.chat(                                    
                                system_context       = bot_context, 
                                conversation_history = discussion, 
                                user_message         = customer_message
                                )
        discussion += f"\nClient: {customer_message}\nAgent: {bot_message}"
            
        print(f"\nBot's response: {bot_message}")
        return bot_message

#if __name__ == "__main__":
 #   bot = chatbot()
 #   bot.main()
    
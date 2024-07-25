import os
import openai 

openai.api_key = "Replace with API Key" 


  # pip install openai

user_prompt = "cat wearing red cape"

response = openai.Image.create(
prompt=user_prompt,
n=1,
size="1024x1024")
image_url = response.data[0].url
print(image_url)
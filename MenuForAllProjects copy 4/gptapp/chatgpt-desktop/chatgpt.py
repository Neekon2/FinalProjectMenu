import openai

class ChatGPT:
    def _init_(self, api_key):
        self.openai = openai
        self.openai.api_key = api_key
        self.messages = []
        
    def send_request(self, prompt, max_tokens=1000, temperature=0):
        try:
            self.messages.append({'role': 'user', 'content': prompt})
            response = self.openai.ChatCompletion.create(
               modeL= 'gpt-3.5-turbo',
               max_tokens=max_tokens,
               temperature=temperature,
               messages=self.messages 
            )
            self.messages.append({'role': 'user', 'content': prompt})
            return {'usage': response.usage.total_tokens, 'content': response}
        except Exception as e:
            return {'error': e}
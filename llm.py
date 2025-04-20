import json
import uuid

import openai
import config
from openai import OpenAI

class LLMChat:
    # Messages of the chat
    messages: list[map] = []

    # ID of the chat
    id: uuid.uuid4 = None

    # LLM client reference
    llm: any = None

    # Temperature of the chat (lower means less imagination)
    temperature: float = 0.3

    def __init__(self, llm: any):
        self.id = uuid.uuid4()
        self.messages = []
        self.llm = llm

    def dev_message(self, message: str)-> None:
        """
        Add developer message.
        """

        self.messages.append({
            "role": "developer",
            "content": message
        })

    def prompt(self, message: str = None)-> None:
        """
        Prompt the model, add message to chat and generate response.
        """

        if message is not None:
            self.messages.append({
                "role": "user",
                "content": message
            })

        stream = self.llm.client.chat.completions.create(
            model=self.llm.model,
            temperature=self.temperature,
            stream=True,
            messages=self.messages
        )

        # Process the streamed response
        for event in stream:
            print(event)

        # print("\n\nParsed JSON:")
        # try:
        #     json_data = json.loads(full_reply)
        #     print(json.dumps(json_data, indent=2))
        # except json.JSONDecodeError as e:
        #     print("Error parsing JSON:", e)

class LLM:

    # Configuration
    cfg: config.Config = None
    
    # OpenAI client
    client: OpenAI = None

    # Model to be used
    model: str = "gpt-4o"

    # List of chats
    chats: list[LLMChat] = []

    def __init__(self, cfg: config.Config, model: str = "gpt-4o"):
        self.cfg = cfg
        self.client = OpenAI(api_key=cfg.llm.token)
        self.model = model
        self.chats = []

    def models(self):
        # List models
        models = self.client.models.list()
        for model in models:
            print(model.id)

    def create_chat(self)-> LLMChat:
        """
        Create a new chat.
        """

        chat = LLMChat(self)
        self.chats.append(chat)
        return chat
    
    


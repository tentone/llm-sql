import json
from typing import Callable
import uuid
import config
from openai import OpenAI

class LLMChat:
    # Messages of the chat
    messages: list[map] = []

    # ID of the chat
    id: uuid.UUID = None

    # LLM client reference
    llm: any = None

    # Temperature of the chat (lower means less imagination)
    temperature: float = 0.4

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

    def prompt(self, message: str = None, on_chunk: Callable = None)-> any:
        """
        Prompt the model, add message to chat and generate response.

        Return the message generated as JSON
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
        result = ""
        for chunk in stream:
            if len(chunk.choices) > 0:
                content = chunk.choices[0].delta.content
                if content is None:
                    break
                
                if on_chunk is not None:
                    on_chunk(content)
                result += content

        json_data = json.loads(result)
        return json_data

class LLMModel:

    # Configuration
    cfg: config.Config = None
    
    # OpenAI client
    client: OpenAI = None

    # Model to be used
    model: str = "gpt-4o-mini"

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
    
    def delete_chat(self, id: uuid.UUID)-> None:
        """
        Delete chat by id
        """

        chat = self.get_chat(id)
        self.chats.remove(chat)


    def get_chat(self, id: uuid.UUID)-> LLMChat:
        """
        Get chat by id.
        """
        for i in range(len(self.chats)):
            if self.chats[i].id == id:
                return self.chats[i]
        
        raise Exception("Chat not found in the model")


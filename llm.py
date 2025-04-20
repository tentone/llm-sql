import json
import uuid
import config
import database
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

    def prompt(self, message: str = None)-> any:
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
        message = ""
        for chunk in stream:
            if len(chunk.choices) > 0:
                content = chunk.choices[0].delta.content
                print(chunk.choices[0])
                # reason = chunk.choices[0].delta.finish_reason
                if content is None: # or reason == 'stop':
                    break

                print(content, end='', flush=True)
                result += content

        print(f"\n\nResult is {result}")

        print("\n\nParsed JSON:")
        try:
            json_data = json.loads(result)
            return json_data
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)

class LLMModel:

    # Configuration
    cfg: config.Config = None
    
    # OpenAI client
    client: OpenAI = None

    # Model to be used
    model: str = "gpt-4o"

    # List of chats
    chats: list[LLMChat] = []

    def __init__(self, cfg: config.Config, db: database.Database, model: str = "gpt-4o"):
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
    
    


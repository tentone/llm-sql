import os
from openai import OpenAI

class LLM:
    cfg: config.Config = None
    
    client: OpenAI = None

    model: str = "gpt-4o"

    def __init__(self, cfg):
        self.cfg = cfg

        self.client = OpenAI(api_key=cfg.llm.token)

    def prompt(self, text: str)-> str:
        """
        Prompt the LLM with a text and get the response.
        """
        response = self.client.responses.create(
            model="gpt-4o",
            input=text
        )

        return response.output_text



from fastapi import FastAPI
import uvicorn
import config
import llm
class API:
    cfg: config.Config

    app: FastAPI

    def __init__(self, cfg: config.Config, l: llm.LLMModel):
        self.cfg = cfg
        self.app = FastAPI()
        self.l = l
        self.setup_routes()

    def setup_routes(self):
        """
        Set up the API routes here.
        """
        @self.app.get("/")
        def hello():
            return {"Hello": "World"}

    def run(self):
        """
        Start the http server
        """
        uvicorn.run(self.app, host=self.cfg.http.host, port=self.cfg.http.port)


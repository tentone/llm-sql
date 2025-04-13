from fastapi import FastAPI
import uvicorn
import config

class API:
    cfg: config.Config

    app: FastAPI

    def __init__(self, cfg: config.Config):
        self.cfg = cfg
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/")
        def read_root():
            return {"Hello": "World"}

    def run(self):
        uvicorn.run(self.app, host=self.cfg.http.host, port=self.cfg.http.port)


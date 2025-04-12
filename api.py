from fastapi import FastAPI
import uvicorn

class API:

    def __init__(self, config):
        self.config = config
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/")
        def read_root():
            return {"Hello": "World"}

    def run(self):
        
        uvicorn.run(self.app, host=self.config.host, port=self.config.port)


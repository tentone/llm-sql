import os
import database
import config
import logging
import llm
import api

logging.basicConfig(level=logging.DEBUG)

logging.info("Read configuration file")
cfg = config.Config()
cfg.load('config.json')

logging.info("Connecting to database")
db = database.Database(cfg)
db.connect()

if os.path.exists("structure.txt"):
    logging.info("Read database structure")
    f = open("structure.txt", "r")
    structure = f.read()
else:
    logging.info("Generate database structure")
    structure = db.database_structure()
    f = open("structure.txt", "w")
    f.write(structure)

logging.info("Read initial prompt file")
f = open("prompt.txt", "r")
initial_prompt = f.read()

logging.info("Connect to OpenAPI service")
l = llm.LLMModel(cfg, "gpt-4o-mini")

c = l.create_chat()
c.dev_message(initial_prompt + structure)
c.prompt("Hello")
c.prompt("Get me all assets")

logging.info("Starting API service")
api = api.API(cfg, l)
api.run()



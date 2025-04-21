import os
import re
import database
import config

import logging
import llm


logging.info("Read configuration file")
cfg = config.Config()
cfg.load('config.json')

if cfg.debug:
    logging.basicConfig(level=logging.DEBUG)

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

output = ""

while True:
    message = input("\n\nMessage (blank to exit): ")
    if len(message) == 0:
        break
    
    output = ""
    printed = ""

    def on_chunk(content: str)-> None:
        global output
        global printed

        output += content
        partial = re.search(r"\"message\"\s*:\s*\"([^\"]*)\"?", output)
        if partial is not None:
            groups = partial.groups()
            if len(groups)> 0:
                group = groups[0]
                
                substring = group[len(printed):]
                printed = group 
                print(substring, end="", flush=True)
    
    print("Assistant: ", end="")
    result = c.prompt(message, on_chunk)
    
    if result['type'] == 'sql':
        print(f"\nSQL query to get the data: {result['query']}")

        table = db.query(result['query'])
        print(table)




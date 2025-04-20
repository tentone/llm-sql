import database
import config
import api
import logging

logging.info("Read configuration file")
cfg = config.Config()
cfg.load('config.json')

logging.info("Connecting to database")
db = database.Database(cfg)
db.connect()



structure = db.database_structure()
print(structure)

# TODO  

logging.info("Starting API service")
api = api.API(cfg)
api.run()



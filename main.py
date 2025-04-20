import database
import config
import api

cfg = config.Config()
cfg.load('config.json')

db = database.Database(cfg)
db.connect()



structure = db.database_structure()
print(structure)

api = api.API(cfg)
api.run()



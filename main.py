import database
import config
import api

cfg = config.Config()
cfg.load('config.json')

db = database.Database(cfg)
db.connect()

result = db.query("SELECT * FROM your_table")
for row in result:
    print(row)


api = api.API(cfg)
api.run()



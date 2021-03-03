import os

from seed.composite_seeder.update_location_composite import UpdateLocationComposite
from src.database import PostgresConnector

db = PostgresConnector(os.environ['DATABASE_URI'])
# so fucking unnecessary -_-
seeder_composite = UpdateLocationComposite(db=db)
seeder_composite.run()

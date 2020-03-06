from flask_script import Manager

from app import app
from commands.seed_data import SeedData

# configure your app

manager = Manager(app)

if __name__ == "__main__":
    manager.add_command('seed_data', SeedData())
    manager.run()

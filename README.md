# SENG3340 Project

## Name (TBD)

A python implemented GUI fighting game.

### Dependencies
For this project we are using python version 3.11.8
`pip install -r requirements.txt`

### Features
- **plotDamage**: Goes through a users attacks to see how much damage they can do to an opponent
- **highestAttack**: Find a players strongest attack against an opponent
- **SortLoot**: Goes through a loot pool (dictionary) and returns an updated dictionary for the player character. (Mitch)
- **PlotRisk**: Determines how much of a risk it is to receive an attack
- **Health**: Encompasses healing and stat restoration mechanics

### Actions
- `pip install black flake8`
- Auto-format with `black .`
- Use `flake8 .` to see lints

### Packaging
- Install pyinstaller (5.13.2)
- Unix: `pyinstaller --noconsole --onefile --add-data "dunwoody_disaster/:dunwoody_disaster/" main.py`
- Windows: Change the `:` to a `;`

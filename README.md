# Searching for Housing with Python

Searching for housing is tedious. I just want to run a server and be notified when there is a good house available.

## Requirements

To run this tool, you will require:
1. A Postgres database and to include the url in the correct file in the `credentials`folder.
2. A google maps api key for the commute time calculations.
3. A GMail account to use with the service so that it can email you.

## Installation

1. Clone the repository on your local machine
2. Make sure you have python3 installed
3. Run a `pip install -r requirements.txt`

## Usage

To run, simply execute `python main.py`


To adjust the kinds of listings you would like to search, in the `main.py` file there are a few hard-coded variables that can be changed to suite different needs in theory, altough this was never tested.


The desired address however can be easily changed and will work correctly

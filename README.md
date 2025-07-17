# Looks Fishy! 

## Description
A simple program that calculates and displays fishing conditions at a location in Norway. The fishing condition is calculated based on what is considered good and bad weather when fishing in freshwater.

The program does not consider or find the best time on the day, it just checks all hours and creates a summary based on the weather for that day. This can be improved upon, as one can have bad conditions at the start of a day and then suddenly very good conditions due to a change in weather. 

### Current rules:
#### Conditions that are considered to be good for fishing:
* Lightrain
* Cloud cover
* Wind from southeast
* Some (a little) wind
* Decent temperature (between 15°C and 25°C)

#### Conditions that are considered to be bad for fishing:
* Direct sun (No cloud cover)
* Heavy rain
* Thunder
* Wind from north
* No wind
* Cold or warm temperature (less than 15°C or more than 25°C)


## Install
1. This project uses UV. Install the tool by following the guide found here: "https://docs.astral.sh/uv/getting-started/installation/"
2. Run command `uv sync --locked --all-extras --dev`

## Usage
1. Run command `uv run src/main.py`



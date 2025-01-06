# DragonQuest 3 Personality Guesser.

This repository contains a Python script designed to optimize seed distribution for achieving desired personality traits in characters. The script takes into account various character classes, genders, and initial stats to determine the best seed distribution for the desired personality outcome. Everything here is based on DragonQuest 3 HD 2D Remake.

## Features

- **Character Classes and Genders**: Supports multiple character classes (Warrior, Martial Artist, Priest, Mage, Thief, Merchant, Gadabout) and genders (Male, Female).
- **Personality Optimization**: Uses a comprehensive personality table to match the best possible personalities based on the two highest stat growths.
- **Command-Line Interface**: Easy-to-use command-line interface for inputting character class, gender, desired personality, and initial stats.
- **Logging**: Configurable logging to track the optimization process and debug if necessary.

## Usage

To run the script, use the following command:
```sh
python dq-figure-out-seed-dist-for-pers.py <class_name> <gender> <desired_personality> <initial_stats>
```

Example:
```sh
python dq-figure-out-seed-dist-for-pers.py "Warrior" "Male" "Paragon" "Strength:13,Agility:6,Resilience:14,Wisdom:4,Luck:6"
```

## Arguments
 - class_name: Character class name (e.g., "Warrior", "Mage").
 - gender: Character gender ("Male" or "Female").
 - desired_personality: Desired personality trait (e.g., "Paragon").
 - initial_stats: Initial stats in the format "Strength:13,Agility:6,Resilience:14,Wisdom:4,Luck:6".

## Requirements
 - Python 3.x
 - argparse
 - logging
 - itertools

## Installation
Clone the repository:
```sh
git clone https://github.com/yourusername/dq-figure-out-seed-dist-for-pers.git
cd dq-figure-out-seed-dist-for-pers
```

## Logging Configuration
The script supports logging to a file. You can enable or disable logging by setting the DEBUG_MODE variable:
```python
# Enable or disable logging
DEBUG_MODE = True

# Configure logging
log_file_path = r'D:\source\repos\ADO Custom Form Extension\Custom-Form-Extension-And-Webapi\Ado-Extension\log.txt'
if DEBUG_MODE:
    logging.basicConfig(level=logging.DEBUG, filename=log_file_path)
else:
    logging.basicConfig(level=logging.CRITICAL, filename=log_file_path)
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

import asyncio
import os
import pyz3r
import json
import yaml
import logging

from config import PRESETS_DIR

# Function to read and parse the YAML preset file
def get_yaml_presets():
    """
    Iterates through the presets directory and returns a list of all the 'goal_name' fields within each file.

    :return: List of preset goals.
    """
    logging.info("Fetching goals from YAML presets")
    presets = []
    for file in os.listdir(PRESETS_DIR):
        if file.endswith('.yaml') or file.endswith('.yml'):
            file_name, ext = os.path.splitext(file)
            presets.append(file_name)
    presets.sort()
    logging.info(f"Found {len(presets)} presets")
    return presets

def read_yaml_preset(preset_name):
    for file in os.listdir(PRESETS_DIR):
        file_name, ext = os.path.splitext(file)
        if file_name == preset_name:
            file_path = os.path.join(PRESETS_DIR, file)
            with open(file_path, 'r') as preset_file:
                yaml_content = yaml.safe_load(preset_file)

            return yaml_content

# Function to convert the YAML content to a settings dictionary
def convert_yaml_to_settings(yaml_content):
    settings = yaml_content.get('settings', {})
    # Add custom logic here to transform the YAML settings
    
    print(settings)
    #settings["mode"] = "race"

    return settings

# Function to convert settings dictionary to JSON and then back to a dictionary
def convert_settings_to_json_and_back(settings_dict):
    json_string = json.dumps(settings_dict)
    return json.loads(json_string)

# Async function to generate the ALTTPR seed
async def generate_alttpr_seed(preset_name):
    # Read and parse the YAML preset file
    preset_content = read_yaml_preset(preset_name)

    # Convert YAML content to settings dictionary
    settings_dict = convert_yaml_to_settings(preset_content)

    # Convert settings dictionary to JSON and back to dictionary
    settings_for_customizer = convert_settings_to_json_and_back(settings_dict)

    # print(settings_for_customizer)

    # Determine the endpoint
    endpoint = '/api/customizer' if preset_content.get('customizer', False) else '/api/randomizer'

    # Generate the seed using pyz3r with the customizer settings
    seed = await pyz3r.ALTTPR.generate(settings=settings_for_customizer, endpoint=endpoint)

    return seed

# Main function to run the async function
async def main_generate(preset_name):
    seed = await generate_alttpr_seed(preset_name)
    return seed

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    seed = loop.run_until_complete(main_generate("casualboots"))
    print(seed.url)

import asyncio
import os
import pyz3r
import json
import yaml
import logging
from pathlib import Path

from alttpr_tool.config import Config

class SeedGenerator:
    """Handles ALTTPR seed generation and preset management"""
    def __init__(self):
        self.config = Config()
    
    def get_yaml_presets(self) -> list:
        """
        Get list of available presets from the presets directory.
        
        Returns:
            list: List of preset names.
        """
        logging.info("Fetching goals from YAML presets")
        presets = []
        for file in os.listdir(self.config.PRESETS_DIR):
            if file.endswith(('.yaml', '.yml')):
                preset_name = Path(file).stem
                presets.append(preset_name)
        presets.sort()
        logging.info(f"Found {len(presets)} presets")
        return presets

    def _read_yaml_preset(self, preset_name: str) -> dict:
        """
        Read and parse a YAML preset file.
        
        Args:
            preset_name: Name of the preset to read.
            
        Returns:
            dict: Parsed YAML content.
        """
        for file in os.listdir(self.config.PRESETS_DIR):
            file_name = Path(file).stem
            if file_name == preset_name:
                file_path = self.config.PRESETS_DIR / file
                with open(file_path, 'r') as preset_file:
                    return yaml.safe_load(preset_file)
        raise FileNotFoundError(f"Preset {preset_name} not found")

    def _convert_yaml_to_settings(self, yaml_content: dict) -> dict:
        """
        Convert YAML content to settings dictionary.
        
        Args:
            yaml_content: Parsed YAML content.
            
        Returns:
            dict: Settings dictionary.
        """
        settings = yaml_content.get('settings', {})
        logging.debug(f"Converted settings: {settings}")
        return settings

    def _convert_settings_to_json_and_back(self, settings_dict: dict) -> dict:
        """
        Convert settings through JSON for compatibility.
        
        Args:
            settings_dict: Settings dictionary.
            
        Returns:
            dict: Processed settings dictionary.
        """
        return json.loads(json.dumps(settings_dict))

    async def generate_alttpr_seed(self, preset_name: str):
        """
        Generate an ALTTPR seed using the specified preset.
        
        Args:
            preset_name: Name of the preset to use.
            
        Returns:
            pyz3r.ALTTPR: Generated seed object.
        """
        preset_content = self._read_yaml_preset(preset_name)
        settings_dict = self._convert_yaml_to_settings(preset_content)
        settings_for_customizer = self._convert_settings_to_json_and_back(settings_dict)

        endpoint = '/api/customizer' if preset_content.get('customizer', False) else '/api/randomizer'
        
        try:
            seed = await pyz3r.ALTTPR.generate(
                settings=settings_for_customizer, 
                endpoint=endpoint
            )
            logging.info(f"Generated seed with preset {preset_name}")
            return seed
        except Exception as e:
            logging.error(f"Failed to generate seed: {e}")
            raise

    async def main_generate(self, preset_name: str):
        """
        Main entry point for seed generation.
        
        Args:
            preset_name: Name of the preset to use.
            
        Returns:
            pyz3r.ALTTPR: Generated seed object.
        """
        return await self.generate_alttpr_seed(preset_name)


# Example usage
if __name__ == "__main__":
    generator = SeedGenerator()
    loop = asyncio.get_event_loop()
    seed = loop.run_until_complete(generator.main_generate("casualboots"))
    print(seed.url)

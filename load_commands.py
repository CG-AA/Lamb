import os
from discord.ext import commands
import importlib
from loguru import logger

def setup_commands(bot: commands.Bot, category_default_enabled: bool = True, exclude_category: list[str] | None = [],command_default_enabled: bool = True, exclude_command: list[str] | None = []):
    if exclude_category is None:
        exclude_category = []
    if exclude_command is None:
        exclude_command = []
    for category in os.listdir("commands"):
        if category.startswith("_") or not os.path.isdir(os.path.join("commands", category)):
            continue
        if category_default_enabled:
            if category in exclude_category:
                continue
        else:
            if category not in exclude_category:
                continue

        for command_file in os.listdir(os.path.join("commands", category)):
            if command_file.startswith("_") or not command_file.endswith(".py"):
                continue
            command_name = command_file[:-3]
            if command_default_enabled:
                if command_name in exclude_command:
                    continue
            else:
                if command_name not in exclude_command:
                    continue
            module_path = f"commands.{category}.{command_name}"
            try:
                module = importlib.import_module(module_path)
                for obj in dir(module):
                    if not obj.startswith("commands_"):
                        continue
                    command_func = getattr(module, obj)
                    if callable(command_func):
                        command_func(bot)
                        logger.info(f"Loaded command: {obj} from {module_path}")
            except ImportError as e:
                logger.error(f"Failed to import {module_path}: {e}")
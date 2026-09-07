from importlib import resources, metadata
import os

__version__ = metadata.version(__package__)

MINGHU6_HOME = os.environ.get("MINGHU6_HOME")
RESOURCES_HOME = resources.files(__package__) / "resources"
TEMPLATES_HOME = RESOURCES_HOME / "templates"

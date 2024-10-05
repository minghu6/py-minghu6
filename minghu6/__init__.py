from os.path import abspath, dirname, join

__version__ = "2.0.0"
MINGHU_HOME = abspath(dirname(__file__))
RESOURCES_HOME = join(dirname(MINGHU_HOME), "resources")
TEMPLATES_HOME = join(RESOURCES_HOME, "templates")

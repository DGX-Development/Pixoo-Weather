import os
from importlib import import_module

from dotenv import dotenv_values


ICON_SET_MODULES = {
    "premium_pixel": "icon_sets.premium_pixel",
    "legacy_pixel": "icon_sets.legacy_pixel",
}

env_icon_set = dotenv_values(".env").get("PIXOO_ICON_SET")
requested_icon_set = os.getenv("PIXOO_ICON_SET", env_icon_set or "premium_pixel")
icon_set_module = import_module(ICON_SET_MODULES.get(requested_icon_set, ICON_SET_MODULES["premium_pixel"]))

ICON_RENDERERS = icon_set_module.ICON_RENDERERS
ICON_SET_NAME = icon_set_module.ICON_SET_NAME


__all__ = ["ICON_RENDERERS", "ICON_SET_NAME"]

#! /usr/bin/env python
"""
"""
import logging
import pkg_resources
from climactic.tag import TagFactory

logger = logging.getLogger(__name__)


ENTRYPOINT = "climactic.plugins"


def load_plugins():
    """
    Utilize entry points to load any plugins.

    :return:
    """
    plugins = {}
    for entrypoint in pkg_resources.iter_entry_points(ENTRYPOINT):
        logger.trace("+ Loaded plugin '{}'", entrypoint.name)
        plugin = entrypoint.load()
        if isinstance(plugin, type):
            plugin = plugin()
        plugins[entrypoint.name] = plugin
        load_tags_from_plugin(plugin)
    return plugins


def load_tags_from_plugin(plugin):
    """
    Check whether the plugin exports any tags,
    and if so, register them with climactic.

    :param plugin:
    :return:
    """
    try:
        tags = plugin.tags
    except AttributeError:
        return

    for tag in tags:
        if isinstance(tag, str):
            tag = getattr(plugin, tag)
        TagFactory.register_tag(tag)

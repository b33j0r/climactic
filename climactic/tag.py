#! /usr/bin/env python
"""
``climactic.tag``
-----------------

A tag is any object which is parsed in input
YAML. Commands and assertions are also tags.

.. autoclass:: TagFactory
"""
import yaml
import logging
import traceback
from yaml.constructor import ConstructorError
from climactic.errors import ClimacticUnknownTagError, ClimacticBug


logger = logging.getLogger(__name__)


class TagFactory:

    """
    Static class; aggregates defined tags, and
    employs the abstract factory pattern to create
    concrete instances of `Tag` objects.

    Generally, `tag_name` is parsed directly from the
    input YAML and associated with a subclass of `Tag`.
    """

    _tag_registry = {}

    @classmethod
    def register_tag(cls, tag_cls):
        already_registered = tag_cls.NAME in cls._tag_registry

        cls._tag_registry[tag_cls.NAME] = tag_cls

        logger.trace(
            "  + Registered tag {!r}", tag_cls.NAME
        )

        if already_registered:
            logger.error(
                "During initialization, tag {!r} was "
                "registered more than once",
                tag_cls.NAME
            )

        # support YAML tag syntax
        def yaml_constructor(loader, node):
            try:
                ctor = tag_cls.yaml_constructor
            except AttributeError:
                ctor = cls.default_yaml_constructor
            spec = ctor(loader, node)
            return tag_cls(spec)

        yaml.add_constructor(
            "!" + tag_cls.NAME,
            yaml_constructor
        )

    @classmethod
    def default_yaml_constructor(cls, loader, node):
        try:
            return loader.construct_mapping(node)
        except ConstructorError:
            pass
        try:
            return loader.construct_sequence(node)
        except ConstructorError:
            pass
        try:
            return loader.construct_scalar(node)
        except ConstructorError:
            raise

    @classmethod
    def build_tag(cls, tag_name, spec):
        try:
            cmd_cls = cls._tag_registry[tag_name]
            return cmd_cls(spec)
        except KeyError:
            raise ClimacticUnknownTagError(
                "Tag {} is not defined".format(tag_name)
            )
        except TypeError:
            raise ClimacticBug(
                (
                    "Tag {} is not implemented correctly"
                    "\n\n"
                    "{}"
                ).format(
                    tag_name,
                    traceback.format_exc()
                )
            )

    @classmethod
    def build_tags(cls, task_dict):
        tags = []
        for tag_name, spec in task_dict.items():
            tag = cls.build_tag(tag_name, spec)
            tags.append(tag)
        return tags

#! /usr/bin/env python
"""
A tag is a more general concept than a command.
It refers to any object which is parsed in input
YAML. Commands are also tags.
"""
import yaml
import logging
import traceback
from abc import ABCMeta
from yaml.constructor import ConstructorError


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
        cls._tag_registry[tag_cls.NAME] = tag_cls

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
            logger.error(
                "Tag %r is not defined", tag_name
            )
        except TypeError:
            logger.error(
                (
                    "Tag %r is not "
                    "implemented correctly\n\n"
                    "%s"
                ), tag_name, traceback.format_exc()
            )

    @classmethod
    def build_tags(cls, task_dict):
        tags = []
        for tag_name, spec in task_dict.items():
            logger.debug(
                "Registered tag %r", tag_name
            )
            tag = cls.build_tag(tag_name, spec)
            tags.append(tag)
        return tags


class TagMeta(ABCMeta):

    """
    Used to automatically register all `Tag` subclasses
    """

    def __init__(cls, cls_name, bases=None, dct=None):
        if not dct.pop("is_abstract", False):
            TagFactory.register_tag(cls)
        super().__init__(cls_name, bases, dct)


class Tag(metaclass=TagMeta):

    """
    Base class for all tags that can be used in
    test YAML files
    """

    is_abstract = True


class NameTag(Tag):

    """
    """

    NAME = "name"

    def __init__(self, spec):
        assert isinstance(spec, str)
        self.value = spec

#! /usr/bin/env python
"""
"""
from pprint import pformat
from pathlib import Path
from collections import Mapping, Sequence

import yaml
from yaml.constructor import ConstructorError
from yaml.scanner import ScannerError

from climactic.tag import Tag, TagFactory
from climactic.errors import (
    ClimacticSyntaxError,
    ClimacticUnknownTagError
)


class Parser:

    """
    Parses climactic YAML files into collections
    of tests, which are collections of tags/commands.

    A YAML file can contain multiple documents,
    so parse_file/parse_stream will always produce
    a collection of tests, even if that collection
    consists of just one test.
    """

    # TODO: now that I'm becoming more familiar with the
    #       structure of PyYaml, this can likely be
    #       better implemented by subclassing its
    #       strategy classes (Loader, Composer, etc.)

    def iparse_file(self, file_path):
        """
        Given a path, parses tests in a YAML file
        and yields them one at a time. Each test is
        an ordered sequence of `Tag` objects.

        :return (generator):
        """
        file_path = Path(file_path)
        with file_path.open() as f:
            yield from self.iparse_stream(f)

    def parse_file(self, file_path):
        """
        Given a path, parses tests in a YAML file
        and returns them all at once in a list. Each
        test is an ordered sequence of `Tag` objects.

        :return (list):
        """
        return list(self.iparse_file(file_path))

    def iparse_stream(self, stream):
        """
        Given a stream (such as a file object), parses
        tests in a YAML file and yields them one at a
        time. Each test is an ordered sequence
        of `Tag` objects.

        :return (generator):
        """
        try:
            loader = yaml.load_all(
                stream, Loader=ClimacticYamlLoader
            )
            for document in loader:
                if not document:
                    continue
                yield self.parse_document(document)
        except ScannerError as exc:
            msg = ("Invalid YAML syntax in input file"
                   "\n{}\n{}\n{}").format(
                exc.context_mark,
                exc.problem.replace(
                    "could not found",
                    "could not find"),
                exc.problem_mark
            )
            raise ClimacticSyntaxError(msg)
        except ConstructorError as exc:
            msg = ("Unknown YAML tag in input file"
                   "\n{}\n{}").format(
                exc.problem,
                exc.problem_mark
            )
            raise ClimacticUnknownTagError(msg)

    def parse_stream(self, stream):
        """
        Given a stream (such as a file object), parses
        tests in a YAML file and returns them all at
        once in a list. Each test is an ordered sequence
        of `Tag` objects.

        :return (list):
        """
        return list(self.iparse_stream(stream))

    def parse_document(self, document):
        if (
            isinstance(document, Sequence) and not
            isinstance(document, (str, bytes))
        ):
            return self.parse_document_sequence(document)
        if isinstance(document, Mapping):
            return self.parse_document_mapping(document)
        raise ValueError(
            (
                "Cannot parse a document of type {} "
                "(did you forget '- ' before the first "
                "tag in the file?)"
            ).format(
                document.__class__.__name__
            )
        )

    def parse_document_sequence(self, document):
        tags = []
        for tag in document:
            if isinstance(tag, Tag):
                tags.append(tag)
                continue
            if not isinstance(tag, dict):
                # TODO: extend PyYaml to provide line context
                raise RuntimeError(
                    ("YAML for tag does not "
                     "evaluate to a mapping:"
                     "\n{}").format(pformat(tag))
                )
            c = TagFactory.build_tags(tag)
            tags.extend(c)
        return tags

    def parse_document_mapping(self, document):
        raise NotImplementedError(
            "Parser.parse_document_mapping"
        )


# from yaml.composer import Composer
# from yaml.constructor import Constructor


class ClimacticYamlLoader(yaml.Loader):

    """
    """

    # def compose_node(self, parent, index):
    #     # TODO: this is where we can hook the line number
    #     #       but we still need to use it somehow
    #     line = self.line
    #     node = super().compose_node(parent, index)
    #     node.__line__ = line + 1
    #     return node

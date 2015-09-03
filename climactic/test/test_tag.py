#! /usr/bin/env python
"""
"""
import climactic.tags.metadata


def test_name_tag_stores_value():
    n = climactic.tags.metadata.NameTag("test NameTag")
    assert n.value == "test NameTag"

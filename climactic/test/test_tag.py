#! /usr/bin/env python
"""
"""
from climactic import tag


def test_name_tag_stores_value():
    n = tag.NameTag("test NameTag")
    assert n.value == "test NameTag"

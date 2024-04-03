#!/usr/bin/env python3

# See LICENSE file for copyright and license details.
# TUM CS Bot - https://github.com/ro-i/tumcsbot

import unittest

from tumcsbot.lib.response import Regex


class RegexTest(unittest.TestCase):
    emoji_names: list[tuple[str, str | None]] = [
        ("test", "test"),
        (":test:", "test"),
        (":tes:t:", None),
        ("test:", None),
        (":test", None),
    ]
    stream_names: list[tuple[str, str | None]] = [
        ("test", "test"),
        ("abc def", "abc def"),
        ('!/"§$& - ("!~EÜ', '!/"§$& - ("!~EÜ'),
        ("#**test**", "test"),
        ("#*test*", "#*test*"),
        ("#**test*", "#**test*"),
        ("#*test**", "#*test**"),
    ]
    user_names: list[tuple[str, str | None]] = [
        ("John Doe", "John Doe"),
        ("John", "John"),
        ("John Multiple Doe", "John Multiple Doe"),
        ("@**John**", "John"),
        ("@_**John Doe**", "John Doe"),
        ("@*John*", None),
        ("@_*John*", None),
        ("@John**", None),
        ("@_John**", None),
        ("@**John", None),
        ("@_**John", None),
        ("Jo\\hn", None),
        ("@**J\\n**", None),
        ('@_**John D"e**', None),
    ]
    user_names_ids: list[tuple[str, tuple[str, int] | None]] = [
        ("@_**John Doe|123**", ("John Doe", 123)),
        ("@**John Doe|456**", ("John Doe", 456)),
        ("@John Doe|123**", None),
        ("@**John Doe|123", None),
    ]

    def test_emoji_names(self) -> None:
        for string, emoji in self.emoji_names:
            self.assertEqual(Regex.get_emoji_name(string), emoji)

    def test_stream_names(self) -> None:
        for string, stream_name in self.stream_names:
            self.assertEqual(Regex.get_stream_name(string), stream_name)

    def test_stream_and_topic_names(self) -> None:
        self.assertIsNone(Regex.get_stream_and_topic_name(""))
        self.assertEqual(Regex.get_stream_and_topic_name("abc"), ("abc", None))
        self.assertEqual(Regex.get_stream_and_topic_name("#**abc**"), ("abc", None))
        self.assertEqual(
            Regex.get_stream_and_topic_name("#**abc>def**"), ("abc", "def")
        )
        self.assertEqual(
            Regex.get_stream_and_topic_name("#**abc>def>ghi**"), ("abc", "def>ghi")
        )
        self.assertEqual(
            Regex.get_stream_and_topic_name("#**>**"), (">", None)
        )  # sadly, those are possible...
        self.assertEqual(Regex.get_stream_and_topic_name("#**>a**"), (">a", None))
        self.assertEqual(Regex.get_stream_and_topic_name("#**a>**"), ("a>", None))

    def test_user_names(self) -> None:
        for string, user_name in self.user_names:
            self.assertEqual(Regex.get_user_name(string), user_name)

    def test_user_names_ids(self) -> None:
        for string, user_name in self.user_names_ids:
            self.assertEqual(Regex.get_user_name(string, get_user_id=True), user_name)

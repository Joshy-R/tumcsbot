#!/usr/bin/env python3

# See LICENSE file for copyright and license details.
# TUM CS Bot - https://github.com/ro-i/tumcsbot

from inspect import cleandoc
from typing import Any, Dict, Iterable, List, Optional, Union

from tumcsbot.lib import split, Response
from tumcsbot.plugin import CommandPlugin


class CreateStreams(CommandPlugin):
    plugin_name = 'create_streams'
    syntax = 'create_streams <stream_name>,<stream_description>...'
    description = cleandoc(
        """
        Create a public stream for every (stream,description)-tuple \
        passed to this command. You may provide a quoted empty string
        as description.
        The (stream name, stream description)-tuples may be separated
        by any whitespace.
        [administrator/moderator rights needed]

        Example:
        ````text
        create_streams "'stream without description',''" "'stream with description','descriptive description'"
        "'next useful stream with \\"quotes\\"','nice'"
        ````

        Notes:
        - It is not yet possible to have single-quotes (`'`) in stream \
        names or descriptions.
        """
        )

    def handle_message(
        self,
        message: Dict[str, Any],
        **kwargs: Any
    ) -> Union[Response, Iterable[Response]]:
        if not self.client.user_is_privileged(message['sender_id']):
            return Response.admin_err(message)

        failed: List[str] = []

        stream_tuples: Optional[List[Any]] = split(
            message['command'], converter = [lambda t: split(
                t, sep = ',', exact_split = 2, discard_empty = False
            )]
        )
        if stream_tuples is None or None in stream_tuples:
            return Response.error(message)

        for stream, desc in stream_tuples:
            if not stream:
                failed.append('one empty stream name')
                continue
            result: Dict[str, Any] = self.client.add_subscriptions(
                streams = [{'name': stream, 'description': desc}]
            )
            if result['result'] != 'success':
                failed.append(f'stream: {stream}, description: {desc}')

        if not failed:
            return Response.ok(message)

        response: str = 'Failed to create the following streams:\n' + '\n'.join(failed)

        return Response.build_message(message, response, msg_type = 'private')

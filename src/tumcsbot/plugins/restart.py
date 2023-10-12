#!/usr/bin/env python3

# See LICENSE file for copyright and license details.
# TUM CS Bot - https://github.com/ro-i/tumcsbot

import os
import signal
from typing import Any, Iterable

from tumcsbot.lib import Response
from tumcsbot.plugin import PluginCommandMixin, PluginThread


class Restart(PluginCommandMixin, PluginThread):
    syntax = "restart"
    description = "Restart the bot.\n[administrator/moderator rights needed]"

    def handle_message(self, message: dict[str, Any]) -> Response | Iterable[Response]:
        if not self.client().user_is_privileged(message["sender_id"]):
            return Response.privilege_err(message)

        # Ask the parent process to restart.
        os.kill(os.getpid(), signal.SIGUSR1)

        # dead code
        return Response.none()

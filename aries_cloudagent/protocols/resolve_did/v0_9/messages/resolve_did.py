"""Resolve DID message."""

from datetime import datetime
from typing import Union

from marshmallow import fields

from .....messaging.agent_message import AgentMessage, AgentMessageSchema
from .....messaging.util import datetime_now, datetime_to_str
from .....messaging.valid import INDY_ISO8601_DATETIME

from ..message_types import RESOLVE, PROTOCOL_PACKAGE

HANDLER_CLASS = f"{PROTOCOL_PACKAGE}.handlers.resolve_did_handler.ResolveDidHandler"


class ResolveDid(AgentMessage):
    """Class defining the structure of a resolve did message."""

    class Meta:
        """Basic message metadata class."""

        handler_class = HANDLER_CLASS
        message_type = RESOLVE
        schema_class = "ResolveDidSchema"

    def __init__(
        self,
        *,
        sent_time: Union[str, datetime] = None,
        did: str = None,
        localization: str = None,
        **kwargs,
    ):
        """
        TODO: update doc
        Initialize basic message object.

        Args:
            sent_time: Time message was sent
            did: did to resolve
            localization: localization

        """
        super().__init__(**kwargs)
        if not sent_time:
            sent_time = datetime_now()
        if localization:
            self._decorators["l10n"] = localization
        self.sent_time = datetime_to_str(sent_time)
        self.did = did


class ResolveDidSchema(AgentMessageSchema):
    """Basic message schema class."""

    class Meta:
        """Resolve DID message schema metadata."""

        model_class = ResolveDid

    sent_time = fields.Str(
        required=False,
        description="Time message was sent, ISO8601 with space date/time separator",
        **INDY_ISO8601_DATETIME,
    )
    did = fields.Str(required=True, description="DID",
                     example="did:sov:WRfXPg8dantKVubE3HX8pw",)

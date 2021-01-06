"""Resolve DID response message."""

# TODO: add further response fields/options, see
# https://github.com/hyperledger/aries-rfcs/tree/master/features/0124-did-resolution-protocol#resolve-message

from datetime import datetime
import json
from typing import Union

from marshmallow import fields

from .....messaging.agent_message import AgentMessage, AgentMessageSchema
from .....messaging.util import datetime_now, datetime_to_str
from .....messaging.valid import INDY_ISO8601_DATETIME

from ..message_types import RESOLVE_RESULT, PROTOCOL_PACKAGE

HANDLER_CLASS = \
    f"{PROTOCOL_PACKAGE}.handlers.resolve_did_result_handler.ResolveDidResultHandler"


class ResolveDidResult(AgentMessage):
    """Class defining the structure of a resolve did message."""

    class Meta:
        """Basic message metadata class."""

        handler_class = HANDLER_CLASS
        message_type = RESOLVE_RESULT
        schema_class = "ResolveDidResultSchema"

    def __init__(
        self,
        *,
        sent_time: Union[str, datetime] = None,
        did_document: str = None,
        localization: str = None,
        **kwargs,
    ):
        """
        TODO: update doc
        Initialize basic message object.

        Args:
            sent_time: Time message was sent
            did_document: did document (as json or python object)
            localization: localization

        """
        super().__init__(**kwargs)
        if not sent_time:
            sent_time = datetime_now()
        if localization:
            self._decorators["l10n"] = localization
        self.sent_time = datetime_to_str(sent_time)
        if not isinstance(did_document, str):
            did_document = json.dumps(did_document)
        self.did_document = did_document


class ResolveDidResultSchema(AgentMessageSchema):
    """Basic message schema class."""

    class Meta:
        """Resolve DID message schema metadata."""

        model_class = ResolveDidResult

    sent_time = fields.Str(
        required=False,
        description="Time message was sent, ISO8601 with space date/time separator",
        **INDY_ISO8601_DATETIME,
    )
    example = '{"@context": "https://w3id.org/did/v0.11", "id": "did:sov:xyz",}'
    did_document = fields.Str(required=True, description="DID",
                              example=example)

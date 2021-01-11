"""Register DID result message."""

from datetime import datetime
from typing import Union

from marshmallow import fields

from .....messaging.agent_message import AgentMessage, AgentMessageSchema
from .....messaging.util import datetime_now, datetime_to_str
from .....messaging.valid import INDY_ISO8601_DATETIME

from ..message_types import REGISTER_RESULT, PROTOCOL_PACKAGE

HANDLER_CLASS = (f"{PROTOCOL_PACKAGE}.handlers.register_did_result_handler."
                 "RegisterDidResultHandler")


class RegisterDidResult(AgentMessage):
    """Class defining the structure of a register did result message."""

    class Meta:
        """Basic message metadata class."""

        handler_class = HANDLER_CLASS
        message_type = REGISTER_RESULT
        schema_class = "RegisterDidResultSchema"

    def __init__(
        self,
        *,
        sent_time: Union[str, datetime] = None,
        job_id: int = None,
        did_state: dict = None,
        registrar_metadata: dict = None,
        method_metadata: dict = None,
        localization: str = None,
        **kwargs,
    ):
        """
        Args:
            sent_time: Time message was sent
            did_document: did_document to register
            localization: localization

        """
        super().__init__(**kwargs)
        if not sent_time:
            sent_time = datetime_now()
        if localization:
            self._decorators["l10n"] = localization
        self.sent_time = datetime_to_str(sent_time)
        self.did_state = did_state
        self.registrar_metadata = registrar_metadata
        self.method_metadata = method_metadata
        self.job_id = job_id


class RegisterDidResultSchema(AgentMessageSchema):
    """Basic message schema class."""

    class Meta:
        """Register DID result message schema metadata."""
        model_class = RegisterDidResult

    sent_time = fields.Str(
        required=False,
        description="Time message was sent, ISO8601 with space date/time separator",
        **INDY_ISO8601_DATETIME,
    )
    job_id = fields.Int(required=False,
                        description="ID of the registration job",
                        example=None,
                        default=None,
                        allow_none=True)
    did_state = fields.Dict(required=True,
                            description="DID registration state",
                            example="finished")
    registrar_metadata = fields.Dict(required=True,
                                     description="Registrar service metadata",
                                     example='{"duration": 40}')
    method_metadata = fields.Dict(required=False,
                                  description="DID method metadata",
                                  example='null',
                                  allow_none=True)

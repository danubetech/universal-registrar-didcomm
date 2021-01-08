"""Resolve DID message."""

from datetime import datetime
from typing import Union

from marshmallow import fields

from .....messaging.agent_message import AgentMessage, AgentMessageSchema
from .....messaging.util import datetime_now, datetime_to_str
from .....messaging.valid import INDY_ISO8601_DATETIME

from ..message_types import REGISTER, PROTOCOL_PACKAGE

HANDLER_CLASS = f"{PROTOCOL_PACKAGE}.handlers.register_did_handler.RegisterDidHandler"


class RegisterDid(AgentMessage):
    """Class defining the structure of a register did message."""

    class Meta:
        """Basic message metadata class."""

        handler_class = HANDLER_CLASS
        message_type = REGISTER
        schema_class = "RegisterDidSchema"

    def __init__(
        self,
        *,
        sent_time: Union[str, datetime] = None,
        job_id: int = None,
        did_document: dict = None,
        driver_id: str = None,
        localization: str = None,
        secret: dict = None,
        options: dict = None,
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
        self.did_document = did_document
        self.driver_id = driver_id
        self.secret = secret
        self.options = options
        self.job_id = job_id


class RegisterDidSchema(AgentMessageSchema):
    """Basic message schema class."""

    class Meta:
        """Register DID message schema metadata."""
        model_class = RegisterDid

    sent_time = fields.Str(
        required=False,
        description="Time message was sent, ISO8601 with space date/time separator",
        **INDY_ISO8601_DATETIME,
    )
    driver_id = fields.Str(required=True, description="Driver ID",
                           example="driver-universalregistrar/driver-did-key")
    job_id = fields.Int(required=False,
                        description="ID of the registration job",
                        example=None,
                        default=None,
                        allow_none=True)
    options = fields.Dict(required=True, description="Registration options",
                          example='{"keyType": "Ed25519VerificationKey2018"}')
    secret = fields.Dict(required=False, description="secret", default={})
    did_document = fields.Dict(required=True,
                               description="DID Document to register",
                               example="TODO")

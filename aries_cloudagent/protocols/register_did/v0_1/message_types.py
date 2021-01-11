"""Message types for DID registration."""

from ...didcomm_prefix import DIDCommPrefix

SPEC_URI = (
    "TODO_NOT_DEFINED"
)

PROTOCOL_URI = "https://didcomm.org/did_registration/0.1"

REGISTER = f"{PROTOCOL_URI}/register"
REGISTER_RESULT = f"{PROTOCOL_URI}/register_result"

PROTOCOL_PACKAGE = "aries_cloudagent.protocols.register_did.v0_1"

MESSAGE_TYPES = DIDCommPrefix.qualify_all(
    {
        REGISTER: f"{PROTOCOL_PACKAGE}.messages.register_did.RegisterDid",
        REGISTER_RESULT:
        f"{PROTOCOL_PACKAGE}.messages.register_did_result.RegisterDidResult"
    }
)

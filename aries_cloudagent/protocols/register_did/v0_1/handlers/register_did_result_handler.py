"""Register DID result message handler."""

from .....messaging.base_handler import BaseHandler, BaseResponder, RequestContext

from ..messages.register_did_result import RegisterDidResult
from .. import REGISTRATION_RESPONSE_OPTIONS


class RegisterDidResultHandler(BaseHandler):
    """Message handler class for register did result messages."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic a did registration result.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug("RegisterDidResultHandler called with context %s",
                           context)
        assert isinstance(context.message, RegisterDidResult)

        self._logger.info("Received register did result")
        self._logger.debug("response content: %s", context.message)

        webhook_content = {
            "connection_id": context.connection_record.connection_id,
            "message_id": context.message._id,
        }
        for key in REGISTRATION_RESPONSE_OPTIONS.keys():
            webhook_content[key] = getattr(context.message, key)
        await responder.send_webhook("register_did_result", webhook_content)

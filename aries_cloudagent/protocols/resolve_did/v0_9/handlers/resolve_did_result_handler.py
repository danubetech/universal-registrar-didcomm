"""Resolve DID result message handler."""

import json

from .....messaging.base_handler import BaseHandler, BaseResponder, RequestContext

from ..messages.resolve_did_result import ResolveDidResult


class ResolveDidResultHandler(BaseHandler):
    """Message handler class for resolve did result messages."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic a did resolve result.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug("ResolveDidResultHandler called with context %s", context)
        assert isinstance(context.message, ResolveDidResult)

        self._logger.info("Received resolve did document")
        self._logger.debug("did document: %s", context.message.did_document)

        did_document = json.loads(context.message.did_document)

        await responder.send_webhook(
            "resolve_did_result",
            {
                "connection_id": context.connection_record.connection_id,
                "message_id": context.message._id,
                "did_document": did_document,
                "state": "received",
            },
        )

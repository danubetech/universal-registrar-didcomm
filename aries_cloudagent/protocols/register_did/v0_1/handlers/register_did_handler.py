"""Register DID message handler."""

import json
import requests

from .....messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
    HandlerException
)

from ..messages.register_did import RegisterDid
# from ..messages.register_did_result import RegisterDidResult
from .. import REGISTRATION_OPTIONS


class RegisterDidHandler(BaseHandler):
    """Message handler class for registering a DID."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for registering a did using a registrar service.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug("RegisterDidHandler called with context %s", context)
        assert isinstance(context.message, RegisterDid)

        self._logger.info("Received register did document: %s",
                          context.message.did_document)

        # TODO: get registrar from settings?
        # registrar_url = context.settings.get("did_registration_service")
        registrar_url = "https://uniregistrar.io/1.0/register"
        registration_options = {key: getattr(context.message, key, None) for
                                key in REGISTRATION_OPTIONS}
        try:
            response = register_did(registrar_url, **registration_options)
            self._logger.info("registration result: %s" % response)
        except Exception as err:
            self._logger.error(str(err))
            msg = (f"Could not register DID {context.message.did} using "
                   f"service {registrar_url}")
            raise HandlerException(msg)
        else:
            """
            TODO: send response via didcomm
            reply_msg = RegisterDidResult(did_document=did_document)
            reply_msg.assign_thread_from(context.message)
            if "l10n" in context.message._decorators:
                reply_msg._decorators["l10n"] = context.message._decorators["l10n"]
            await responder.send_reply(reply_msg)
            """


def register_did(url, job_id, did_document, driver_id, options, secret):
    """Register a DID using a registrar service like uniregistrar."""
    import pdb
    pdb.set_trace()
    params = {"driverId": "driver-universalregistrar/driver-did-key"}
    payload = {
        "jobId": job_id,
        "options": options,
        "secret": secret,
        "didDocument": did_document
    }
    response = requests.post(url, params=params, data=json.dumps(payload))
    if response.ok:
        return response.json()
    raise HandlerException(f"Failed to register DID document using URL {url}")

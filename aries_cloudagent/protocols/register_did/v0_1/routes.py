"""DID resolution routes."""

from aiohttp import web
from aiohttp_apispec import docs, request_schema

from marshmallow import fields, Schema

from ....admin.request_context import AdminRequestContext
from ....connections.models.conn_record import ConnRecord
from ....storage.error import StorageNotFoundError

from .messages.register_did import RegisterDid
from . import REGISTRATION_OPTIONS


class RegisterDidSchema(Schema):
    """Request schema for registering a DID."""
    driver_id = fields.Str(required=True, description="Driver ID",
                           example="driver-universalregistrar/driver-did-key")
    job_id = fields.Int(required=False,
                        description="ID of the registration job",
                        example="null",
                        default=None,
                        allow_none=True)
    options = fields.Dict(required=True, description="Registration options",
                          example='{"keyType": "Ed25519VerificationKey2018"}')
    secret = fields.Dict(required=False, description="secret", default={})
    did_document = fields.Dict(required=True,
                               description="DID Document to register",
                               example="TODO")


@docs(tags=["registerdid"], summary="Register a DID via a DID registrar")
@request_schema(RegisterDidSchema())
async def connections_register_did(request: web.BaseRequest):
    """
    Request handler to register a DID using a local or remote registrar.

    Args:
        request: aiohttp request object

    """
    context: AdminRequestContext = request["context"]
    connection_id = request.match_info["id"]
    outbound_handler = request["outbound_message_router"]
    params = await request.json()

    try:
        async with context.session() as session:
            connection = await ConnRecord.retrieve_by_id(session, connection_id)
    except StorageNotFoundError:
        raise web.HTTPNotFound()

    if not connection.is_ready:
        raise web.HTTPBadRequest(reason=f"Connection {connection_id} not ready")

    registration_options = {key: params[key] for key in REGISTRATION_OPTIONS 
                            if key in params}
    msg = RegisterDid(**registration_options)
    await outbound_handler(msg, connection_id=connection_id)

    return web.json_response({})


async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [web.post("/connections/{id}/register-did", connections_register_did)]
    )

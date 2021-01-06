"""DID resolution routes."""

from aiohttp import web
from aiohttp_apispec import docs, request_schema

from marshmallow import fields, Schema


from ....connections.models.conn_record import ConnRecord
from ....storage.error import StorageNotFoundError

from .messages.resolve_did import ResolveDid


class ResolveDidSchema(Schema):
    """Request schema for resolving a DID."""

    did = fields.Str(description="DID",
                     example="did:sov:WRfXPg8dantKVubE3HX8pw")


@docs(tags=["resolvedid"], summary="Resolve a DID via a DID resolver")
@request_schema(ResolveDidSchema())
async def connections_resolve_did(request: web.BaseRequest):
    """
    Request handler to resolve a DID using a local or remote resolving service.

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

    msg = ResolveDid(did=params["did"])
    await outbound_handler(msg, connection_id=connection_id)

    return web.json_response({})


async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [web.post("/connections/{id}/resolve-did", connections_resolve_did)]
    )

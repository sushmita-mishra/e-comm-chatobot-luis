from http import HTTPStatus
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import(
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity

from config import DefaultConfig
from dialogs import MainDialog
from bots import DialogAndWelcomeBot

from adapter_with_error_handler import AdapterWithErrorHandler

from dialogs.operations.createorder_dialog import CreateOrderDialog
from dialogs.operations.vieworder_dialog import ViewOrderDialog
from dialogs.operations.cancelorder_dialog import CancelOrderDialog
from dialogs.operations.completeorder_dialog import CompleteOrderDialog


CONFIG = DefaultConfig()

SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)

MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

#create adapter
ADAPTER = AdapterWithErrorHandler(SETTINGS, CONVERSATION_STATE)

COMPLETEORDER_DIALOG = CompleteOrderDialog()
CREATEORDER_DIALOG = CreateOrderDialog(COMPLETEORDER_DIALOG)
VIEWORDER_DIALOG = ViewOrderDialog()
CANCELORDER_DIALOG = CancelOrderDialog()

DIALOG = MainDialog(CREATEORDER_DIALOG, VIEWORDER_DIALOG, CANCELORDER_DIALOG)
BOT = DialogAndWelcomeBot(CONVERSATION_STATE, USER_STATE, DIALOG)


#Listen for incoming requests on /api/messages.
async def messages(req: Request)-> Response:
    #Main bor message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)

    return Response(status = HTTPStatus.OK)

APP =  web.Application(middlewares = [aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(APP, host = "localhost", port = CONFIG.PORT)
    except Exception as error:
        raise error

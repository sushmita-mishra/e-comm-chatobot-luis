from botbuilder.core import StatePropertyAccessor, TurnContext 
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus

from user_details import UserDetails

class DialogHelper:
    @staticmethod
    async def run_dialog(
        dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)
        user_details = UserDetails()
        user_details.user_id = None
        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog.id, user_details)

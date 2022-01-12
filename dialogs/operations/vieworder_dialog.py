from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, ConfirmPrompt
from botbuilder.core import MessageFactory, TurnContext, CardFactory, UserState
from botbuilder.schema import InputHints, CardAction, ActionTypes, SuggestedActions

import orderApp
import pandas as pd


class ViewOrderDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(ViewOrderDialog, self).__init__(dialog_id or ViewOrderDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__, [self.view_step,]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def view_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        user_id = user_details.user_id

        df = pd.DataFrame()
        df = orderApp.getOrders(user_id)

        for ind in df.index:
            msg_text = "Order ID: " + df['order_id'][ind]
            msg_text = msg_text + " - " + df['order_description'][ind] + " - STATUS: " + df['order_status'][ind]
            msg = MessageFactory.text(msg_text, msg_text, InputHints.ignoring_input)

            await step_context.context.send_activity(msg)
        
        return await step_context.end_dialog(user_details)
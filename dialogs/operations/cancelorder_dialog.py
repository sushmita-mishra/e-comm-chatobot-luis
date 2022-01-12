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

class CancelOrderDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(CancelOrderDialog, self).__init__(dialog_id or CancelOrderDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__, [self.intro_step, self.act_step]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        message_text = "Please provide the order id you want to delete."
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        user_id = user_details.user_id

        order_id = step_context.result

        msg_text = orderApp.cancelOrder(user_id, order_id)

        msg = MessageFactory.text(msg_text, msg_text, InputHints.ignoring_input)

        await step_context.context.send_activity(msg)

        return await step_context.end_dialog(user_details)

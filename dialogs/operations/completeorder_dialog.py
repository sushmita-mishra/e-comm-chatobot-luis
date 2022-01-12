from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints

import json
import requests

class CompleteOrderDialog(ComponentDialog):
    def __init__(self, dialog_id:str = None):
        super(CompleteOrderDialog, self).__init__(dialog_id or CompleteOrderDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [self.flavour_step, self.quantity_step, self.size_step, self.summary_step]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def flavour_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options

        

        if len(user_details.orders_list) > 0 and len(user_details.orders_list) > int(user_details.current_order):
            order_details = user_details.orders_list[int(user_details.current_order)]

            if order_details.item_flavour is None:
                message_text = "Please provide the flavour for item " + order_details.item_name + "."
                prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
                return await step_context.prompt(
                    TextPrompt.__name__, PromptOptions(prompt=prompt_message)
                )

        return await step_context.next(user_details)

    async def quantity_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options

        if type(step_context.result) == str:
                
                user_details.orders_list[int(user_details.current_order)].item_flavour = step_context.result
 

        if len(user_details.orders_list) > 0 and len(user_details.orders_list) > int(user_details.current_order):
            order_details = user_details.orders_list[int(user_details.current_order)]
           

            if order_details.item_quantity is None or len(order_details.item_quantity.strip()) == 0 or order_details.item_quantity.strip() == "\"":
             
                message_text = "Please provide the quantity for item " + order_details.item_name + "."
                prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
                return await step_context.prompt(
                    TextPrompt.__name__, PromptOptions(prompt=prompt_message)
                )

        return await step_context.next(user_details)

    async def size_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options

        if type(step_context.result) == str:
                user_details.orders_list[int(user_details.current_order)].item_quantity = step_context.result

        if len(user_details.orders_list) > 0 and len(user_details.orders_list) > int(user_details.current_order):
            order_details = user_details.orders_list[int(user_details.current_order)]       

            if str(order_details.item_name).upper() == "CAKE" and (order_details.item_size is None):
             
                message_text = "Please provide the size for item " + order_details.item_name + "."
                prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
                return await step_context.prompt(
                    TextPrompt.__name__, PromptOptions(prompt=prompt_message)
                )

        return await step_context.next(user_details)

    
    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options

        if type(step_context.result) == str:
                user_details.orders_list[int(user_details.current_order)].item_size = step_context.result
        
        user_details.current_order = int(user_details.current_order) + 1

        if len(user_details.orders_list) > 0 and len(user_details.orders_list) > int(user_details.current_order):
            order_details = user_details.orders_list[int(user_details.current_order)]

            return await step_context.replace_dialog(self.id, user_details)
        else:

            return await step_context.end_dialog(user_details)

    
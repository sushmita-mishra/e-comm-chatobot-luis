from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, ConfirmPrompt
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints

from .completeorder_dialog import CompleteOrderDialog
from order_details import OrderDetails

import pandas as pd
import string
import random
import orderApp
from datetime import date

import luisApp


class CreateOrderDialog(ComponentDialog):
    def __init__(self, completeorder_dialog: CompleteOrderDialog, dialog_id:str = None):
        super(CreateOrderDialog, self).__init__(dialog_id or CreateOrderDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self._completeorder_dialog_id = completeorder_dialog.id
        self.add_dialog(completeorder_dialog)

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [self.order_step, self.act_step, self.completeorder_step, self.summary_step]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def order_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        message_text = "Please provide the order details."
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    
    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        user_id = user_details.user_id
        order_desc = str(step_context.result)

        user_details.orders_list = []


        data = luisApp.getLuisResponse(order_desc)

        
        orders = data['prediction']['entities']['order']

        for order in orders:
            obj_order = OrderDetails()
            if 'item_name' in order:
                obj_order.item_name = order['item_name'][0]
            if 'item_quantity' in order:
                obj_order.item_quantity = order['item_quantity'][0] 
            if 'item_flavour' in order:
                obj_order.item_flavour = order['item_flavour'][0]
            if 'item_size' in order:
                obj = order['item_size'][0]
                size_value = None
                size_unit = None
                if 'size_value' in obj:
                    size_value = str(obj['size_value'][0]) + " "
                if 'size_unit' in obj:
                    size_unit = obj['size_unit'][0]
                obj_order.item_size = size_value + size_unit  

            user_details.orders_list.append(obj_order)

        for o in user_details.orders_list:
            print("item name : ", o.item_name)
            print("item quantity : ", o.item_quantity)
            print("item flavour : ", o.item_flavour)
            print("item size : ", o.item_size)

        user_details.current_order = 0

        

        return await step_context.next(user_details)


    async def completeorder_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options

        if len(user_details.orders_list) > 0:
            

            return await step_context.begin_dialog(self._completeorder_dialog_id, user_details)
        
        else:
            return await step_context.next(user_details)



    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        user_details = step_context.options
        user_id = user_details.user_id
        #generate order id
        N = 4
        order_id = ''.join(random.choices(string.digits, k= N))
        order_id = 'ord' + order_id
        order_date =date.today()
        order_status = "Order Received"

        df = pd.DataFrame()
        items = []

        

        print("print the data:")
        for o in user_details.orders_list:
            order = o.item_quantity + " " + o.item_flavour + " " + o.item_name 
            if o.item_size:
                order = order + " " + o.item_size
            print(order)

            items.append(order)

        df['order_description'] = items
        df['user_id'] = user_id
        df['order_id'] = order_id
        df['order_status'] = order_status
        df['creation_date'] = order_date
        

        orderApp.addOrders(df)

        msg_text = ("Your order number is " + order_id + ". Here are the orders provided-")

        msg = MessageFactory.text(
            msg_text, msg_text, InputHints.ignoring_input
        )
        await step_context.context.send_activity(msg)

        for i in range(0, len(items)):
            msg_text = (items[i])
            msg = MessageFactory.text(msg_text, msg_text, InputHints.ignoring_input)
            await step_context.context.send_activity(msg)
        

        return await step_context.end_dialog(user_details)
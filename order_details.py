class OrderDetails:
    def __init__(
        self,
        item_name: str = None,
        item_quantity: str = None,
        item_size: str = None,
        item_flavour: str = None,
    ):
        
        self.item_name = item_name
        self.item_quantity= item_quantity
        self.item_size = item_size
        self.item_flavour = item_flavour
class UserDetails:
    def __init__(
        self,
        user_id: str = None,
        orders_list: [] = [],
        current_order: int = 0,
    ):
        self.user_id = user_id
        self.orders_list = orders_list
        self.current_order = current_order
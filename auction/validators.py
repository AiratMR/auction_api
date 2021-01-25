class AuctionBidValidator:

    @staticmethod
    def is_valid_price(last_price, new_price, price_step) -> bool:
        """
        New bid price validation
        :param last_price: last price of goods
        :param new_price: new price of goods
        :param price_step: auction price step
        :return: validation result
        """
        if new_price - last_price >= price_step:
            return True
        return False

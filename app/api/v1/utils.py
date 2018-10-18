from flask import abort


class Validate:
    def validate_type(self, price, quantity):
        if price < 0 or quantity < 0:
            abort(400,  "price or quantity should be a positive integer")

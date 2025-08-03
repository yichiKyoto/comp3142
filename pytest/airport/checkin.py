# airport/checkin.py

class Suitcase:
    def __init__(self, length, width, height):
        self.length = length
        self.width =  width
        self.height = height

    

class Gate:
    def __init__(self, width=99999, height=99999):
        self.width = width
        self.height = height

    # This function returns the price of the given suitcase by dimension size.
    def check_price(self, case: Suitcase):
        return NotImplementedError("This method is not implemented yet.")

    def can_pass_gate(self, x, y):
        return (
            (self.width >= x and self.height >= y) or
            (self.height >= x and self.width >= y)
        )


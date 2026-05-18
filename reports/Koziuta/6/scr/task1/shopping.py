class Cart:
    """Shopping cart with items and prices."""

    def __init__(self):
        self.items = {}

    def add_item(self, name: str, price: float, quantity: int = 1):
        """Add an item or increase quantity."""
        if price <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive")
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name: str, quantity: int = 1):
        """Remove given quantity of an item."""
        if name not in self.items:
            raise KeyError(f"Item {name} not in cart")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.items[name]["quantity"] < quantity:
            raise ValueError(f"Cannot remove {quantity}, only {self.items[name]['quantity']} available")
        self.items[name]["quantity"] -= quantity
        if self.items[name]["quantity"] == 0:
            del self.items[name]

    def total(self) -> float:
        """Calculate total price."""
        return sum(item["price"] * item["quantity"] for item in self.items.values())

    def clear(self):
        """Remove all items."""
        self.items.clear()

    def __len__(self):
        return sum(item["quantity"] for item in self.items.values())

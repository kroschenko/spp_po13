from abc import ABC, abstractmethod
from typing import List, Optional

class Pizza:

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.price} rub.)"

    def get_price(self) -> float:
        return self.price


class Order:

    def __init__(self, order_id: int):
        self.id = order_id
        self.pizzas: List[Pizza] = []
        self.total = 0.0
        self.status = "created"

    def add_pizza(self, pizza: Pizza):
        self.pizzas.append(pizza)
        self.total += pizza.price

    def confirm(self):
        self.status = "confirmed"
        print(f"Order #{self.id} confirmed. Total: {self.total} rub.")

    def cancel(self):
        self.status = "cancelled"
        print(f"Order #{self.id} cancelled.")


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class CreateOrderCommand(Command):

    def __init__(self, pizzeria: 'Pizzeria', pizzas: List[Pizza]):
        self._pizzeria = pizzeria
        self._pizzas = pizzas
        self._order: Optional[Order] = None

    def execute(self):
        self._order = self._pizzeria.create_order(self._pizzas)
        return self._order

    def undo(self):
        if self._order:
            self._pizzeria.cancel_order(self._order.id)


class CancelOrderCommand(Command):

    def __init__(self, pizzeria: 'Pizzeria', order_id: int):
        self._pizzeria = pizzeria
        self._order_id = order_id
        self._cancelled_order: Optional[Order] = None

    def execute(self):
        self._cancelled_order = self._pizzeria.cancel_order(self._order_id)
        return self._cancelled_order

    def undo(self):
        if self._cancelled_order:
            self._pizzeria.restore_order(self._cancelled_order)


class RepeatOrderCommand(Command):

    def __init__(self, pizzeria: 'Pizzeria', original_order: Order):
        self._pizzeria = pizzeria
        self._original_order = original_order
        self._new_order: Optional[Order] = None

    def execute(self):
        if self._original_order.status == "cancelled":
            print(f"Cannot repeat cancelled order #{self._original_order.id}")
            return None

        self._new_order = self._pizzeria.create_order(self._original_order.pizzas.copy())
        print(f"Repeated order #{self._original_order.id} -> new order #{self._new_order.id}")
        return self._new_order

    def undo(self):
        if self._new_order:
            self._pizzeria.cancel_order(self._new_order.id)


class Pizzeria:

    def __init__(self, name: str):
        self.name = name
        self.orders: List[Order] = []
        self._next_id = 1
        self._history: List[Command] = []

    def create_order(self, pizzas: List[Pizza]) -> Order:
        order = Order(self._next_id)
        self._next_id += 1
        for pizza in pizzas:
            order.add_pizza(pizza)
        order.confirm()
        self.orders.append(order)
        return order

    def cancel_order(self, order_id: int) -> Optional[Order]:
        for order in self.orders:
            if order.id == order_id and order.status != "cancelled":
                order.cancel()
                return order
        print(f"Order #{order_id} not found or already cancelled.")
        return None

    def restore_order(self, order: Order):
        if order.status == "cancelled":
            order.status = "confirmed"
            print(f"Order #{order.id} restored.")
            if order not in self.orders:
                self.orders.append(order)

    def execute_command(self, command: Command):
        result = command.execute()
        self._history.append(command)
        return result

    def undo_last_command(self):
        if self._history:
            cmd = self._history.pop()
            cmd.undo()
            print("Last operation undone.")
        else:
            print("No commands to undo.")

    def show_orders(self):
        print(f"\n=== Orders in {self.name} ===")
        if not self.orders:
            print("No orders.")
        for order in self.orders:
            pizzas_str = ", ".join(str(p) for p in order.pizzas)
            print(f"  #{order.id}: [{pizzas_str}] - {order.total} rub. ({order.status})")


if __name__ == "__main__":
    pizzeria_obj = Pizzeria("Pizza Hut")

    margherita = Pizza("Margherita", 450)
    pepperoni = Pizza("Pepperoni", 550)
    four_cheese = Pizza("Four Cheese", 600)

    print("\nCreating order")
    create_cmd = CreateOrderCommand(pizzeria_obj, [margherita, pepperoni])
    order1 = pizzeria_obj.execute_command(create_cmd)

    print("\nCancelling order")
    cancel_cmd = CancelOrderCommand(pizzeria_obj, order1.id)
    pizzeria_obj.execute_command(cancel_cmd)

    print("\nCreating another order")
    create_cmd2 = CreateOrderCommand(pizzeria_obj, [four_cheese])
    order2 = pizzeria_obj.execute_command(create_cmd2)

    print("\nRepeat order #2")
    repeat_cmd = RepeatOrderCommand(pizzeria_obj, order2)
    order3 = pizzeria_obj.execute_command(repeat_cmd)

    print("\nUndo last command (repeat)")
    pizzeria_obj.undo_last_command()

    pizzeria_obj.show_orders()

    print("\nUndo cancellation (restore order #1)")
    pizzeria_obj.undo_last_command()
    pizzeria_obj.show_orders()

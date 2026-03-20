from abc import ABC, abstractmethod

class Product(ABC):
    @abstractmethod
    def get_name(self):
        pass

class Chocolate(Product):
    def get_name(self):
        return "Chocolate bar" [cite: 31]

class Chips(Product):
    def get_name(self):
        return "Chips" [cite: 33]

class Juice(Product):
    def get_name(self):
        return "Juice" [cite: 35]

class ProductFactory:
    @staticmethod
    def create_product(product_type):
        if product_type == "chocolate":
            return Chocolate() [cite: 39]
        elif product_type == "chips":
            return Chips() [cite: 41]
        elif product_type == "juice":
            return Juice() [cite: 44]
        return None

class VendingMachine:
    def order_product(self, product_type):
        product = ProductFactory.create_product(product_type) [cite: 50]
        if product:
            print("Dispensing:", product.get_name()) [cite: 51]
        else:
            print("Product not available") [cite: 53]

def main():
    vending_machine = VendingMachine() [cite: 55]
    while True:
        print("\nSelect product:")
        print("1 - Chocolate")
        print("2 - Chips")
        print("3 - Juice")
        print("0 - Exit")
        
        choice = input("Enter choice: ") [cite: 67]
        if choice == "1":
            vending_machine.order_product("chocolate") [cite: 69]
        elif choice == "2":
            vending_machine.order_product("chips") [cite: 71]
        elif choice == "3":
            vending_machine.order_product("juice") [cite: 73]
        elif choice == "0":
            print("Goodbye!") [cite: 75]
            break
        else:
            print("Invalid choice") [cite: 80]

if __name__ == "__main__":
    main()

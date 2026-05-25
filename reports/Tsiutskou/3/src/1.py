class Sedan:
    def drive(self):
        pass


class Hatchback:
    def drive(self):
        pass


class ToyotaSedan(Sedan):
    def drive(self):
        return "Toyota Camry"


class ToyotaHatchback(Hatchback):
    def drive(self):
        return "Toyota Corolla"


class TeslaSedan(Sedan):
    def drive(self):
        return "Tesla Model 3"


class TeslaHatchback(Hatchback):
    def drive(self):
        return "Tesla Model Y"


class CarFactory:
    def create_sedan(self):
        pass

    def create_hatchback(self):
        pass


class ToyotaFactory(CarFactory):
    def create_sedan(self):
        return ToyotaSedan()

    def create_hatchback(self):
        return ToyotaHatchback()


class TeslaFactory(CarFactory):
    def create_sedan(self):
        return TeslaSedan()

    def create_hatchback(self):
        return TeslaHatchback()


def produce_cars(factory, name):
    print(f"\nЗавод {name}:")
    print(factory.create_sedan().drive())
    print(factory.create_hatchback().drive())


produce_cars(ToyotaFactory(), "Toyota")
produce_cars(TeslaFactory(), "Tesla")

class Girlfriend:
    def __init__(self, name, age, rate_per_hour, bio):
        self.name = name
        self.age = age
        self.rate_per_hour = rate_per_hour
        self.bio = bio
        self.available = True

    def __str__(self):
        return (f"Name: {self.name}, Age: {self.age}, Rate/Hour: ${self.rate_per_hour}, "
                f"Bio: {self.bio}, Available: {'Yes' if self.available else 'No'}")


class Customer:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def __str__(self):
        return f"Customer: {self.name}, Balance: ${self.balance}"


class RentalSystem:
    def __init__(self):
        self.girlfriends = []
        self.customers = []
        self.rentals = []

    def add_girlfriend(self, name, age, rate_per_hour, bio):
        girlfriend = Girlfriend(name, age, rate_per_hour, bio)
        self.girlfriends.append(girlfriend)

    def add_customer(self, name, balance):
        customer = Customer(name, balance)
        self.customers.append(customer)

    def list_girlfriends(self):
        if not self.girlfriends:
            print("No girlfriends available.")
            return
        print("Available Girlfriends:")
        for i, gf in enumerate(self.girlfriends, start=1):
            print(f"{i}. {gf}")

    def rent_girlfriend(self, customer_name, girlfriend_name, hours):
        customer = next((c for c in self.customers if c.name == customer_name), None)
        girlfriend = next((g for g in self.girlfriends if g.name == girlfriend_name), None)

        if not customer:
            print("Customer not found!")
            return
        if not girlfriend:
            print("Girlfriend not found!")
            return
        if not girlfriend.available:
            print("This girlfriend is currently unavailable.")
            return

        total_cost = hours * girlfriend.rate_per_hour
        if customer.balance < total_cost:
            print("Insufficient balance!")
            return

        customer.balance -= total_cost
        girlfriend.available = False
        self.rentals.append((customer_name, girlfriend_name, hours))
        print(f"{customer_name} has rented {girlfriend_name} for {hours} hour(s) at ${total_cost}.")

    def return_girlfriend(self, girlfriend_name):
        girlfriend = next((g for g in self.girlfriends if g.name == girlfriend_name), None)
        if not girlfriend or girlfriend.available:
            print("This girlfriend is not currently rented.")
            return

        girlfriend.available = True
        print(f"{girlfriend_name} is now available again.")

    def delete_renting(self, customer_name, girlfriend_name):
        rental = next((r for r in self.rentals if r[0] == customer_name and r[1] == girlfriend_name), None)
        if not rental:
            print("Rental not found!")
            return

        girlfriend = next((g for g in self.girlfriends if g.name == girlfriend_name), None)
        if girlfriend:
            girlfriend.available = True
        self.rentals.remove(rental)
        print(f"Rental of {girlfriend_name} by {customer_name} has been deleted.")

    def update_booking(self, customer_name, girlfriend_name, new_hours):
        rental = next((r for r in self.rentals if r[0] == customer_name and r[1] == girlfriend_name), None)
        customer = next((c for c in self.customers if c.name == customer_name), None)
        girlfriend = next((g for g in self.girlfriends if g.name == girlfriend_name), None)

        if not rental:
            print("Rental not found!")
            return

        if not customer or not girlfriend:
            print("Customer or girlfriend not found!")
            return

        current_hours = rental[2]
        additional_hours = new_hours - current_hours
        additional_cost = additional_hours * girlfriend.rate_per_hour

        if customer.balance < additional_cost:
            print("Insufficient balance to update booking!")
            return

        customer.balance -= additional_cost
        self.rentals.remove(rental)
        self.rentals.append((customer_name, girlfriend_name, new_hours))
        print(f"Booking updated: {girlfriend_name} rented by {customer_name} for {new_hours} hour(s). Additional cost: ${additional_cost}.")

    def view_rentals(self):
        if not self.rentals:
            print("No active rentals.")
            return

        print("Active Rentals:")
        for customer_name, girlfriend_name, hours in self.rentals:
            print(f"Customer: {customer_name}, Girlfriend: {girlfriend_name}, Hours: {hours}")

    def list_customers(self):
        if not self.customers:
            print("No customers registered.")
            return
        print("Registered Customers:")
        for customer in self.customers:
            print(customer)


def main():
    system = RentalSystem()

    # Preloaded customers
    customers = [
        ("Amir", 500), ("Aiman", 400), ("Zahir", 600), 
        ("Hafizi", 350), ("Fathi", 450), ("Iqbal", 300)
    ]

    for name, balance in customers:
        system.add_customer(name, balance)

    # Preloaded girlfriends
    girlfriends = [
        ("Ara", 25, 50, "Loves movies and hiking."),
        ("Ilya", 24, 40, "Expert in fine dining and museums."),
        ("Farah", 23, 45, "Passionate about art and poetry."),
        ("Ain", 22, 35, "Enjoys outdoor adventures."),
        ("Balqis", 26, 55, "A foodie who loves exploring cafes.")
    ]

    for name, age, rate_per_hour, bio in girlfriends:
        system.add_girlfriend(name, age, rate_per_hour, bio)

    while True:
        print("\n--- Rent-a-Girlfriend System ---")
        print("1. List Girlfriends")
        print("2. List Customers")
        print("3. Rent Girlfriend")
        print("4. Return Girlfriend")
        print("5. View Rentals")
        print("6. Delete Renting")
        print("7. Update Booking")
        print("8. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            system.list_girlfriends()

        elif choice == "2":
            system.list_customers()

        elif choice == "3":
            customer_name = input("Enter customer name: ")
            girlfriend_name = input("Enter girlfriend name: ")
            hours = int(input("Enter rental hours: "))
            system.rent_girlfriend(customer_name, girlfriend_name, hours)

        elif choice == "4":
            girlfriend_name = input("Enter girlfriend name to return: ")
            system.return_girlfriend(girlfriend_name)

        elif choice == "5":
            system.view_rentals()

        elif choice == "6":
            customer_name = input("Enter customer name: ")
            girlfriend_name = input("Enter girlfriend name: ")
            system.delete_renting(customer_name, girlfriend_name)

        elif choice == "7":
            customer_name = input("Enter customer name: ")
            girlfriend_name = input("Enter girlfriend name: ")
            new_hours = int(input("Enter new rental hours: "))
            system.update_booking(customer_name, girlfriend_name, new_hours)

        elif choice == "8":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

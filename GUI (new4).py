import tkinter as tk
from tkinter import messagebox

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
        self.girlfriends.append(Girlfriend(name, age, rate_per_hour, bio))

    def add_customer(self, name, balance):
        self.customers.append(Customer(name, balance))

    def rent_girlfriend(self, customer_name, girlfriend_name, hours):
        customer = next((c for c in self.customers if c.name == customer_name), None)
        girlfriend = next((g for g in self.girlfriends if g.name == girlfriend_name), None)

        if not customer:
            return "Customer not found!"
        if not girlfriend:
            return "Girlfriend not found!"
        if not girlfriend.available:
            return "This girlfriend is currently unavailable."

        total_cost = hours * girlfriend.rate_per_hour
        if customer.balance < total_cost:
            return "Insufficient balance!"

        customer.balance -= total_cost
        girlfriend.available = False
        self.rentals.append((customer_name, girlfriend_name, hours))
        return f"{customer_name} has rented {girlfriend_name} for {hours} hour(s) at ${total_cost}."

    def return_girlfriend(self, girlfriend_name):
        girlfriend = next((g for g in self.girlfriends if g.name == girlfriend_name), None)
        if not girlfriend or girlfriend.available:
            return "This girlfriend is not currently rented."

        girlfriend.available = True
        return f"{girlfriend_name} is now available again."

    def delete_booking(self, customer_name, girlfriend_name):
        rental = next((r for r in self.rentals if r[0] == customer_name and r[1] == girlfriend_name), None)
        if not rental:
            return "Rental not found!"

        girlfriend = next((g for g in self.girlfriends if g.name == girlfriend_name), None)
        if girlfriend:
            girlfriend.available = True
        self.rentals.remove(rental)
        return f"Rental of {girlfriend_name} by {customer_name} has been deleted."

    def update_booking(self, customer_name, girlfriend_name, new_hours):
        rental = next((r for r in self.rentals if r[0] == customer_name and r[1] == girlfriend_name), None)
        customer = next((c for c in self.customers if c.name == customer_name), None)
        girlfriend = next((g for g in self.girlfriends if g.name == girlfriend_name), None)

        if not rental:
            return "Rental not found!"

        if not customer or not girlfriend:
            return "Customer or girlfriend not found!"

        current_hours = rental[2]
        additional_hours = new_hours - current_hours
        additional_cost = additional_hours * girlfriend.rate_per_hour

        if customer.balance < additional_cost:
            return "Insufficient balance to update booking!"

        customer.balance -= additional_cost
        self.rentals.remove(rental)
        self.rentals.append((customer_name, girlfriend_name, new_hours))
        return f"Booking updated: {girlfriend_name} rented by {customer_name} for {new_hours} hour(s). Additional cost: ${additional_cost}."

    def view_rentals(self):
        if not self.rentals:
            return "No active rentals."

        return "\n".join([f"Customer: {c}, Girlfriend: {g}, Hours: {h}" for c, g, h in self.rentals])

class App:
    def __init__(self, root, system):
        self.system = system
        self.root = root
        self.root.title("Rent-a-Girlfriend System")

        # Main Menu
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()

        tk.Button(self.menu_frame, text="List Girlfriends", command=self.list_girlfriends).pack(fill=tk.X)
        tk.Button(self.menu_frame, text="List Customers", command=self.list_customers).pack(fill=tk.X)
        tk.Button(self.menu_frame, text="Rent Girlfriend", command=self.rent_girlfriend).pack(fill=tk.X)
        tk.Button(self.menu_frame, text="Return Girlfriend", command=self.return_girlfriend).pack(fill=tk.X)
        tk.Button(self.menu_frame, text="View Rentals", command=self.view_rentals).pack(fill=tk.X)
        tk.Button(self.menu_frame, text="Update Booking", command=self.update_booking).pack(fill=tk.X)
        tk.Button(self.menu_frame, text="Delete Booking", command=self.delete_booking).pack(fill=tk.X)
        tk.Button(self.menu_frame, text="Exit", command=root.quit).pack(fill=tk.X)

        self.output_text = tk.Text(root, height=15, width=50)
        self.output_text.pack()

    def list_girlfriends(self):
        self.output_text.delete(1.0, tk.END)
        if not self.system.girlfriends:
            self.output_text.insert(tk.END, "No girlfriends available.")
        else:
            for gf in self.system.girlfriends:
                self.output_text.insert(tk.END, str(gf) + "\n")

    def list_customers(self):
        self.output_text.delete(1.0, tk.END)
        if not self.system.customers:
            self.output_text.insert(tk.END, "No customers registered.")
        else:
            for customer in self.system.customers:
                self.output_text.insert(tk.END, str(customer) + "\n")

    def rent_girlfriend(self):
        self._create_input_window("Rent Girlfriend", self._process_rent)

    def return_girlfriend(self):
        self._create_input_window("Return Girlfriend", self._process_return, inputs=["Girlfriend Name"])

    def view_rentals(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, self.system.view_rentals())

    def update_booking(self):
        self._create_input_window("Update Booking", self._process_update_booking, inputs=["Customer Name", "Girlfriend Name", "New Hours"])

    def delete_booking(self):
        self._create_input_window("Delete Booking", self._process_delete_booking, inputs=["Customer Name", "Girlfriend Name"])

    def _create_input_window(self, title, callback, inputs=["Customer Name", "Girlfriend Name", "Hours"]):
        input_window = tk.Toplevel(self.root)
        input_window.title(title)

        entries = {}
        for inp in inputs:
            tk.Label(input_window, text=inp).pack()
            entry = tk.Entry(input_window)
            entry.pack()
            entries[inp] = entry

        def submit():
            data = {key: entry.get() for key, entry in entries.items()}
            callback(data, input_window)

        tk.Button(input_window, text="Submit", command=submit).pack()

    def _process_rent(self, data, window):
        try:
            hours = int(data["Hours"])
            message = self.system.rent_girlfriend(data["Customer Name"], data["Girlfriend Name"], hours)
        except ValueError:
            message = "Hours must be a number."
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)
        window.destroy()

    def _process_return(self, data, window):
        message = self.system.return_girlfriend(data["Girlfriend Name"])
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)
        window.destroy()

    def _process_update_booking(self, data, window):
        try:
            new_hours = int(data["New Hours"])
            message = self.system.update_booking(data["Customer Name"], data["Girlfriend Name"], new_hours)
        except ValueError:
            message = "New Hours must be a number."
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)
        window.destroy()

    def _process_delete_booking(self, data, window):
        message = self.system.delete_booking(data["Customer Name"], data["Girlfriend Name"])
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)
        window.destroy()

# Preloaded data
system = RentalSystem()
customers = [
    ("Amir", 500), ("Aiman", 400), ("Zahir", 600), 
    ("Hafizi", 350), ("Fathi", 450), ("Iqbal", 300)
]

girlfriends = [
    ("Ara", 25, 50, "Loves movies and hiking."),
    ("Ilya", 24, 40, "Expert in fine dining and museums."),
    ("Farah", 23, 45, "Passionate about art and poetry."),
    ("Ain", 22, 35, "Enjoys outdoor adventures."),
    ("Balqis", 26, 55, "A foodie who loves exploring cafes.")
]

for name, balance in customers:
    system.add_customer(name, balance)

for name, age, rate_per_hour, bio in girlfriends:
    system.add_girlfriend(name, age, rate_per_hour, bio)

# Run the application
root = tk.Tk()
app = App(root, system)
root.mainloop()

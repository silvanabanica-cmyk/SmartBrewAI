"""Main window and login screen for the SmartBrew AI prototype."""

import tkinter as tk
from tkinter import ttk, messagebox

from accounts import create_account, authenticate_user
from assistant import get_assistant_response
from database import (
    initialize_database,
    seed_inventory,
    check_ingredient_availability,
    get_inventory,
    refill_inventory,
    log_waste,
    get_waste_logs,
    save_preferences,
    get_preferences,
    place_order,
    get_user_transactions,
    save_custom_recipe,
    get_custom_recipes,
)


BEVERAGES = {
    "Espresso": {
        "price": 2.00,
        "ingredients": {"Coffee": 20},
    },
    "Americano": {
        "price": 2.50,
        "ingredients": {"Coffee": 20, "Water": 150},
    },
    "Cappuccino": {
        "price": 3.00,
        "ingredients": {"Coffee": 20, "Milk": 100, "Water": 30},
    },
    "Latte": {
        "price": 3.50,
        "ingredients": {"Coffee": 20, "Milk": 180, "Water": 30},
    },
    "Hot Chocolate": {
        "price": 3.00,
        "ingredients": {"Milk": 180, "Chocolate": 25},
    },
}


def show_main_window(root, current_user_id):
    """Display the drink-ordering interface for the logged-in user.

    Args:
        root: The main Tkinter window.
        current_user_id: ID of the authenticated user.
    """
    for widget in root.winfo_children():
        widget.destroy()

    root.title("SmartBrew AI")
    root.geometry("850x780")
    root.minsize(720, 650)

    title_label = ttk.Label(
        root,
        text="SmartBrew AI",
        font=("Arial", 22, "bold"),
    )
    title_label.pack(pady=(12, 4))

    subtitle_label = ttk.Label(
        root,
        text="Customize your drink, discover recommendations, and order.",
    )
    subtitle_label.pack(pady=(0, 10))

    customization_frame = ttk.LabelFrame(
        root,
        text="Customize your drink",
        padding=10,
    )
    customization_frame.pack(fill="x", padx=15, pady=5)

    ttk.Label(customization_frame, text="Beverage:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )

    beverage_var = tk.StringVar(value="Latte")
    beverage_dropdown = ttk.Combobox(
        customization_frame,
        textvariable=beverage_var,
        values=list(BEVERAGES.keys()),
        state="readonly",
        width=22,
    )
    beverage_dropdown.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(customization_frame, text="Coffee strength:").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )

    strength_var = tk.StringVar(value="Medium")
    strength_dropdown = ttk.Combobox(
        customization_frame,
        textvariable=strength_var,
        values=["Mild", "Medium", "Strong"],
        state="readonly",
        width=22,
    )
    strength_dropdown.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(customization_frame, text="Milk:").grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )

    milk_var = tk.StringVar(value="Regular")
    milk_dropdown = ttk.Combobox(
        customization_frame,
        textvariable=milk_var,
        values=["None", "Regular", "Oat", "Soy", "Lactose-free"],
        state="readonly",
        width=22,
    )
    milk_dropdown.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(customization_frame, text="Temperature:").grid(
        row=3, column=0, sticky="w", padx=5, pady=5
    )

    temperature_var = tk.StringVar(value="Hot")
    temperature_dropdown = ttk.Combobox(
        customization_frame,
        textvariable=temperature_var,
        values=["Hot", "Warm", "Iced"],
        state="readonly",
        width=22,
    )
    temperature_dropdown.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(customization_frame, text="Syrup:").grid(
        row=4, column=0, sticky="w", padx=5, pady=5
    )

    syrup_var = tk.StringVar(value="None")
    syrup_dropdown = ttk.Combobox(
        customization_frame,
        textvariable=syrup_var,
        values=["None", "Vanilla", "Caramel", "Hazelnut", "Chocolate"],
        state="readonly",
        width=22,
    )
    syrup_dropdown.grid(row=4, column=1, sticky="w", padx=5, pady=5)

    recipe_frame = ttk.LabelFrame(
        root,
        text="Custom recipe",
        padding=10,
    )
    recipe_frame.pack(fill="x", padx=15, pady=5)

    ttk.Label(recipe_frame, text="Recipe name:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )

    recipe_name_var = tk.StringVar()
    recipe_name_entry = ttk.Entry(
        recipe_frame,
        textvariable=recipe_name_var,
        width=25,
    )
    recipe_name_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(recipe_frame, text="Saved recipes:").grid(
        row=0, column=2, sticky="w", padx=5, pady=5
    )

    saved_recipe_var = tk.StringVar()
    saved_recipe_dropdown = ttk.Combobox(
        recipe_frame,
        textvariable=saved_recipe_var,
        state="readonly",
        width=25,
    )
    saved_recipe_dropdown.grid(row=0, column=3, sticky="w", padx=5, pady=5)

    result_frame = ttk.LabelFrame(
        root,
        text="Drink information",
        padding=10,
    )
    result_frame.pack(fill="both", expand=True, padx=15, pady=5)

    result_text = tk.Text(
        result_frame,
        height=8,
        wrap="word",
        state="disabled",
    )
    result_text.pack(fill="both", expand=True)

    def display_result(message):
        """Show a message in the drink information area.

        Args:
            message: Text to display.
        """
        result_text.configure(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, message)
        result_text.configure(state="disabled")

    def get_current_customizations():
        """Return the currently selected drink customization values.

        Returns:
            A dictionary containing the drink's customization settings.
        """
        return {
            "coffee_strength": strength_var.get(),
            "milk": milk_var.get(),
            "temperature": temperature_var.get(),
            "syrup": syrup_var.get(),
        }

    def get_current_order_details():
        """Build a description of the selected drink and its customizations.

        Returns:
            A dictionary containing the beverage and customization settings.
        """
        return {
            "beverage": beverage_var.get(),
            **get_current_customizations(),
        }

    def preview_drink():
        """Display the selected drink, price, and ingredient availability."""
        beverage = beverage_var.get()
        details = get_current_order_details()
        price = BEVERAGES[beverage]["price"]
        ingredients = BEVERAGES[beverage]["ingredients"]

        try:
            available, message = check_ingredient_availability(ingredients)
        except Exception as error:
            messagebox.showerror(
                "Inventory error",
                f"Could not check ingredient availability:\n{error}",
            )
            return

        availability_message = (
            "Available to order" if available else f"Unavailable: {message}"
        )

        display_result(
            f"Selected drink: {beverage}\n"
            f"Price: {price:.2f}\n"
            f"Coffee strength: {details['coffee_strength']}\n"
            f"Milk: {details['milk']}\n"
            f"Temperature: {details['temperature']}\n"
            f"Syrup: {details['syrup']}\n\n"
            f"Ingredient check: {availability_message}"
        )

    def save_current_preferences():
        """Save the current customization choices for the logged-in user."""
        try:
            details = get_current_customizations()
            save_preferences(
                current_user_id,
                details["coffee_strength"],
                details["milk"],
                details["temperature"],
                details["syrup"],
            )
            messagebox.showinfo(
                "Preferences saved",
                "Your drink preferences have been saved.",
            )
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not save preferences:\n{error}",
            )

    def load_saved_preferences():
        """Load the user's saved preferences into the customization controls."""
        try:
            preferences = get_preferences(current_user_id)

            if not preferences:
                messagebox.showinfo(
                    "No preferences",
                    "You have not saved any preferences yet.",
                )
                return

            strength_var.set(preferences["coffee_strength"])
            milk_var.set(preferences["milk"])
            temperature_var.set(preferences["temperature"])
            syrup_var.set(preferences["syrup"])

            messagebox.showinfo(
                "Preferences loaded",
                "Your saved preferences have been loaded.",
            )
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not load preferences:\n{error}",
            )

    def refresh_saved_recipes():
        """Refresh the recipe dropdown using the user's saved recipes."""
        try:
            recipes = get_custom_recipes(current_user_id)
            saved_recipe_dropdown["values"] = [
                recipe["name"] for recipe in recipes
            ]

            if recipes:
                if saved_recipe_var.get() not in saved_recipe_dropdown["values"]:
                    saved_recipe_var.set(recipes[0]["name"])
            else:
                saved_recipe_var.set("")
        except Exception as error:
            messagebox.showerror(
                "Recipe error",
                f"Could not load saved recipes:\n{error}",
            )

    def save_recipe():
        """Save the current drink customizations as a named recipe."""
        recipe_name = recipe_name_var.get().strip()

        if not recipe_name:
            messagebox.showwarning(
                "Recipe name required",
                "Enter a name for your custom recipe.",
            )
            return

        details = get_current_customizations()

        try:
            success, message = save_custom_recipe(
                current_user_id,
                recipe_name,
                beverage_var.get(),
                details["coffee_strength"],
                details["milk"],
                details["temperature"],
                details["syrup"],
            )

            if success:
                refresh_saved_recipes()
                messagebox.showinfo("Recipe saved", message)
            else:
                messagebox.showwarning("Recipe not saved", message)
        except Exception as error:
            messagebox.showerror(
                "Recipe error",
                f"Could not save the recipe:\n{error}",
            )

    def load_recipe():
        """Load the selected saved recipe into the customization controls."""
        recipe_name = saved_recipe_var.get()

        if not recipe_name:
            messagebox.showwarning(
                "Select a recipe",
                "Choose a saved recipe first.",
            )
            return

        try:
            recipes = get_custom_recipes(current_user_id)
            selected_recipe = next(
                (recipe for recipe in recipes if recipe["name"] == recipe_name),
                None,
            )

            if selected_recipe is None:
                messagebox.showwarning(
                    "Recipe not found",
                    "The selected recipe could not be found.",
                )
                refresh_saved_recipes()
                return

            beverage_var.set(selected_recipe["beverage"])
            strength_var.set(selected_recipe["coffee_strength"])
            milk_var.set(selected_recipe["milk"])
            temperature_var.set(selected_recipe["temperature"])
            syrup_var.set(selected_recipe["syrup"])

            preview_drink()
        except Exception as error:
            messagebox.showerror(
                "Recipe error",
                f"Could not load the recipe:\n{error}",
            )

    def recommend_drinks():
        """Recommend available drinks using the user's saved preferences."""
        try:
            preferences = get_preferences(current_user_id)
        except Exception as error:
            messagebox.showerror(
                "Recommendation error",
                f"Could not load your preferences:\n{error}",
            )
            return

        if not preferences:
            messagebox.showinfo(
                "Save preferences first",
                "Save your drink preferences to receive personalized "
                "recommendations.",
            )
            return

        available_drinks = []

        for beverage, information in BEVERAGES.items():
            try:
                available, _ = check_ingredient_availability(
                    information["ingredients"]
                )
            except Exception as error:
                messagebox.showerror(
                    "Inventory error",
                    f"Could not check ingredients:\n{error}",
                )
                return

            if not available:
                continue

            score = 0
            if beverage in ("Espresso", "Americano") and (
                preferences["coffee_strength"] == "Strong"
            ):
                score += 1

            if beverage in ("Latte", "Cappuccino") and (
                preferences["milk"] != "None"
            ):
                score += 1

            if beverage == "Hot Chocolate" and (
                preferences["coffee_strength"] == "Mild"
            ):
                score += 1

            if preferences["temperature"] == "Iced":
                score += 1

            if preferences["syrup"] != "None":
                score += 1

            available_drinks.append((score, beverage))

        if not available_drinks:
            display_result(
                "No drinks can currently be recommended because the "
                "required ingredients are unavailable."
            )
            return

        available_drinks.sort(key=lambda item: item[0], reverse=True)
        top_score = available_drinks[0][0]
        recommendations = [
            beverage
            for score, beverage in available_drinks
            if score == top_score
        ]

        display_result(
            "Personalized drink recommendations\n\n"
            + "\n".join(
                f"• {beverage} — {BEVERAGES[beverage]['price']:.2f}"
                for beverage in recommendations
            )
            + "\n\nRecommendations are based on your saved preferences "
            "and current ingredient availability."
        )


    def open_assistant():
        """Open a chat window for questions about SmartBrew."""
        chat_window = tk.Toplevel(root)
        chat_window.title("SmartBrew Assistant")
        chat_window.geometry("500x500")
        chat_window.minsize(400, 350)

        ttk.Label(
            chat_window,
            text="SmartBrew Assistant",
            font=("Arial", 16, "bold"),
        ).pack(pady=(12, 5))

        chat_display = tk.Text(
            chat_window,
            wrap="word",
            state="disabled",
        )
        chat_display.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=8,
        )

        input_frame = ttk.Frame(chat_window, padding=10)
        input_frame.pack(fill="x")

        question_var = tk.StringVar()
        question_entry = ttk.Entry(
            input_frame,
            textvariable=question_var,
        )
        question_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8),
        )

        def add_chat_message(sender, message):
            """Append a message to the conversation display.

            Args:
                sender: Label identifying the speaker.
                message: Message text to display.
            """
            chat_display.configure(state="normal")
            chat_display.insert(tk.END, f"{sender}: {message}\n\n")
            chat_display.configure(state="disabled")
            chat_display.see(tk.END)

        def send_question():
            """Send the entered question to the local assistant."""
            question = question_var.get().strip()

            if not question:
                return

            question_var.set("")
            add_chat_message("You", question)

            try:
                preferences = get_preferences(current_user_id)
                response = get_assistant_response(
                    message=question,
                    beverages=BEVERAGES,
                    preferences=preferences,
                    availability_checker=check_ingredient_availability,
                )
            except Exception as error:
                response = (
                    "Sorry, I couldn't process that question. "
                    f"Details: {error}"
                )

            add_chat_message("Assistant", response)

        ttk.Button(
            input_frame,
            text="Send",
            command=send_question,
        ).pack(side="right")

        question_entry.bind("<Return>", lambda event: send_question())
        question_entry.focus_set()

        add_chat_message(
            "Assistant",
            "Hello! Ask me about drinks, prices, ingredients, "
            "availability, preferences, or ordering.",
        )


    def open_technician_dashboard():
        """Open a dashboard for inventory, refills, and waste records."""
        dashboard = tk.Toplevel(root)
        dashboard.title("SmartBrew Technician Dashboard")
        dashboard.geometry("850x620")
        dashboard.minsize(650, 450)

        ttk.Label(
            dashboard,
            text="Technician Dashboard",
            font=("Arial", 18, "bold"),
        ).pack(pady=(12, 4))

        ttk.Label(
            dashboard,
            text="Monitor stock levels, refill ingredients, and record waste.",
        ).pack(pady=(0, 10))

        inventory_frame = ttk.LabelFrame(
            dashboard,
            text="Current Inventory",
            padding=10,
        )
        inventory_frame.pack(fill="both", expand=True, padx=12, pady=6)

        inventory_columns = ("ingredient", "quantity", "threshold", "status")
        inventory_table = ttk.Treeview(
            inventory_frame,
            columns=inventory_columns,
            show="headings",
            height=6,
        )

        for column, heading, width in [
            ("ingredient", "Ingredient", 180),
            ("quantity", "Quantity remaining", 180),
            ("threshold", "Minimum threshold", 180),
            ("status", "Stock status", 180),
        ]:
            inventory_table.heading(column, text=heading)
            inventory_table.column(column, width=width, anchor="center")

        inventory_table.pack(fill="both", expand=True)

        def refresh_inventory():
            """Refresh the inventory table from the database."""
            for item in inventory_table.get_children():
                inventory_table.delete(item)

            try:
                inventory = get_inventory()
            except Exception as error:
                messagebox.showerror(
                    "Inventory error",
                    f"Could not load inventory:\n{error}",
                    parent=dashboard,
                )
                return

            for ingredient, details in inventory.items():
                quantity = details["quantity"]
                threshold = details["threshold"]
                status = (
                    "LOW STOCK"
                    if quantity <= threshold
                    else "OK"
                )

                inventory_table.insert(
                    "",
                    "end",
                    values=(
                        ingredient,
                        f"{quantity:g}",
                        f"{threshold:g}",
                        status,
                    ),
                )

        refill_frame = ttk.LabelFrame(
            dashboard,
            text="Refill Inventory",
            padding=10,
        )
        refill_frame.pack(fill="x", padx=12, pady=6)

        ttk.Label(refill_frame, text="Ingredient:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        ingredient_var = tk.StringVar(value="Coffee")
        ingredient_dropdown = ttk.Combobox(
            refill_frame,
            textvariable=ingredient_var,
            values=["Coffee", "Water", "Milk", "Chocolate"],
            state="readonly",
            width=18,
        )
        ingredient_dropdown.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(refill_frame, text="Quantity to add:").grid(
            row=0, column=2, padx=5, pady=5, sticky="w"
        )

        refill_quantity_var = tk.StringVar()
        ttk.Entry(
            refill_frame,
            textvariable=refill_quantity_var,
            width=12,
        ).grid(row=0, column=3, padx=5, pady=5)

        def refill_selected_ingredient():
            """Validate and add stock for the selected ingredient."""
            try:
                quantity = float(refill_quantity_var.get())
            except ValueError:
                messagebox.showwarning(
                    "Invalid quantity",
                    "Enter a valid positive number.",
                    parent=dashboard,
                )
                return

            if quantity <= 0:
                messagebox.showwarning(
                    "Invalid quantity",
                    "The refill quantity must be greater than zero.",
                    parent=dashboard,
                )
                return

            success, message = refill_inventory(
                ingredient_var.get(),
                quantity,
            )

            if success:
                refill_quantity_var.set("")
                refresh_inventory()
                messagebox.showinfo(
                    "Refill successful",
                    message,
                    parent=dashboard,
                )
            else:
                messagebox.showwarning(
                    "Refill unsuccessful",
                    message,
                    parent=dashboard,
                )

        ttk.Button(
            refill_frame,
            text="Add stock",
            command=refill_selected_ingredient,
        ).grid(row=0, column=4, padx=5, pady=5)

        waste_frame = ttk.LabelFrame(
            dashboard,
            text="Record Wasted Ingredients",
            padding=10,
        )
        waste_frame.pack(fill="x", padx=12, pady=6)

        ttk.Label(waste_frame, text="Ingredient:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        waste_ingredient_var = tk.StringVar(value="Coffee")
        ttk.Combobox(
            waste_frame,
            textvariable=waste_ingredient_var,
            values=["Coffee", "Water", "Milk", "Chocolate"],
            state="readonly",
            width=18,
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(waste_frame, text="Quantity wasted:").grid(
            row=0, column=2, padx=5, pady=5, sticky="w"
        )

        waste_quantity_var = tk.StringVar()
        ttk.Entry(
            waste_frame,
            textvariable=waste_quantity_var,
            width=12,
        ).grid(row=0, column=3, padx=5, pady=5)

        def record_waste():
            """Validate and save a waste entry for the selected ingredient."""
            try:
                quantity = float(waste_quantity_var.get())
            except ValueError:
                messagebox.showwarning(
                    "Invalid quantity",
                    "Enter a valid positive number.",
                    parent=dashboard,
                )
                return

            if quantity <= 0:
                messagebox.showwarning(
                    "Invalid quantity",
                    "The waste quantity must be greater than zero.",
                    parent=dashboard,
                )
                return

            success, message = log_waste(
                waste_ingredient_var.get(),
                quantity,
            )

            if success:
                waste_quantity_var.set("")
                refresh_inventory()
                refresh_waste_logs()
                messagebox.showinfo(
                    "Waste recorded",
                    message,
                    parent=dashboard,
                )
            else:
                messagebox.showwarning(
                    "Waste not recorded",
                    message,
                    parent=dashboard,
                )

        ttk.Button(
            waste_frame,
            text="Record waste",
            command=record_waste,
        ).grid(row=0, column=4, padx=5, pady=5)

        waste_log_frame = ttk.LabelFrame(
            dashboard,
            text="Recent Waste Records",
            padding=10,
        )
        waste_log_frame.pack(fill="both", expand=True, padx=12, pady=6)

        waste_columns = ("id", "ingredient", "quantity", "date")
        waste_table = ttk.Treeview(
            waste_log_frame,
            columns=waste_columns,
            show="headings",
            height=4,
        )

        for column, heading, width in [
            ("id", "Record ID", 80),
            ("ingredient", "Ingredient", 180),
            ("quantity", "Quantity wasted", 180),
            ("date", "Date", 250),
        ]:
            waste_table.heading(column, text=heading)
            waste_table.column(column, width=width, anchor="center")

        waste_table.pack(fill="both", expand=True)

        def refresh_waste_logs():
            """Refresh the waste table using saved database records."""
            for item in waste_table.get_children():
                waste_table.delete(item)

            try:
                records = get_waste_logs()
            except Exception as error:
                messagebox.showerror(
                    "Waste log error",
                    f"Could not load waste records:\n{error}",
                    parent=dashboard,
                )
                return

            for record in records:
                waste_table.insert(
                    "",
                    "end",
                    values=(
                        record["id"],
                        record["waste_type"],
                        f"{record['quantity']:g}",
                        record["created_at"],
                    ),
                )

        refresh_inventory()
        refresh_waste_logs()


    def show_transaction_history():
        """Display previous orders belonging to the logged-in user."""
        try:
            transactions = get_user_transactions(current_user_id)
        except Exception as error:
            messagebox.showerror(
                "Transaction history error",
                f"Could not load transaction history:\n{error}",
            )
            return

        history_window = tk.Toplevel(root)
        history_window.title("Order History")
        history_window.geometry("750x500")
        history_window.minsize(550, 350)

        ttk.Label(
            history_window,
            text="Your Order History",
            font=("Arial", 16, "bold"),
        ).pack(pady=(12, 8))

        if not transactions:
            ttk.Label(
                history_window,
                text="You have not placed any orders yet.",
            ).pack(pady=20)
            return

        table_frame = ttk.Frame(history_window, padding=10)
        table_frame.pack(fill="both", expand=True)

        columns = (
            "id",
            "date",
            "beverage",
            "amount",
            "payment",
            "status",
        )

        order_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "id": "Order ID",
            "date": "Date",
            "beverage": "Drink",
            "amount": "Price",
            "payment": "Payment",
            "status": "Status",
        }

        widths = {
            "id": 65,
            "date": 145,
            "beverage": 140,
            "amount": 75,
            "payment": 90,
            "status": 100,
        }

        for column in columns:
            order_table.heading(column, text=headings[column])
            order_table.column(
                column,
                width=widths[column],
                minwidth=55,
                anchor="center",
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=order_table.yview,
        )
        order_table.configure(yscrollcommand=scrollbar.set)

        order_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for transaction in transactions:
            order_table.insert(
                "",
                "end",
                values=(
                    transaction["id"],
                    transaction["created_at"],
                    transaction["beverage"],
                    f"{transaction['amount']:.2f}",
                    transaction["payment_method"],
                    transaction["status"],
                ),
            )

        details_frame = ttk.LabelFrame(
            history_window,
            text="Selected order details",
            padding=10,
        )
        details_frame.pack(fill="x", padx=10, pady=(0, 10))

        details_text = tk.Text(
            details_frame,
            height=5,
            wrap="word",
            state="disabled",
        )
        details_text.pack(fill="x")

        def display_selected_order(event=None):
            """Show the stored details of the selected transaction."""
            selection = order_table.selection()

            if not selection:
                return

            values = order_table.item(selection[0], "values")
            selected_id = int(values[0])

            transaction = next(
                (
                    item for item in transactions
                    if item["id"] == selected_id
                ),
                None,
            )

            if transaction is None:
                return

            details_text.configure(state="normal")
            details_text.delete("1.0", tk.END)
            details_text.insert(
                tk.END,
                f"Order ID: {transaction['id']}\n"
                f"Date: {transaction['created_at']}\n"
                f"Drink: {transaction['beverage']}\n"
                f"Order details: {transaction['order_details']}\n"
                f"Price: {transaction['amount']:.2f}\n"
                f"Payment method: {transaction['payment_method']}\n"
                f"Status: {transaction['status']}",
            )
            details_text.configure(state="disabled")

        order_table.bind("<<TreeviewSelect>>", display_selected_order)


    def order_drink():
        """Confirm a simulated payment and place the selected drink order."""
        beverage = beverage_var.get()
        details = get_current_order_details()
        ingredients = BEVERAGES[beverage]["ingredients"]
        amount = BEVERAGES[beverage]["price"]

        try:
            available, availability_message = check_ingredient_availability(
                ingredients
            )
        except Exception as error:
            messagebox.showerror(
                "Inventory error",
                f"Could not check ingredient availability:\n{error}",
            )
            return

        if not available:
            messagebox.showwarning(
                "Drink unavailable",
                f"This drink cannot be ordered.\n{availability_message}",
            )
            return

        order_summary = (
            f"Drink: {beverage}\n"
            f"Coffee strength: {details['coffee_strength']}\n"
            f"Milk: {details['milk']}\n"
            f"Temperature: {details['temperature']}\n"
            f"Syrup: {details['syrup']}\n"
            f"Total: {amount:.2f}\n\n"
            "This is a simulated payment. No real money will be charged.\n\n"
            "Confirm order?"
        )

        if not messagebox.askyesno("Confirm order", order_summary):
            return

        try:
            success, message = place_order(
                current_user_id,
                beverage,
                details,
                amount,
                ingredients,
            )

            if success:
                messagebox.showinfo(
                    "Order successful",
                    f"Payment simulated successfully.\n\n"
                    f"Receipt\n"
                    f"Drink: {beverage}\n"
                    f"Amount: {amount:.2f}\n"
                    f"Payment method: Demo\n"
                    f"Status: Completed\n\n"
                    f"{message}",
                )
                preview_drink()
            else:
                messagebox.showwarning("Order unsuccessful", message)
        except Exception as error:
            messagebox.showerror(
                "Order error",
                f"Could not complete the order:\n{error}",
            )

    # Keep the action buttons at the bottom and arrange them in multiple rows.
    button_frame = ttk.Frame(root, padding=(5, 5))
    button_frame.pack(side="bottom", fill="x", padx=15, pady=(0, 8))

    buttons = [
        ("Preview drink", preview_drink),
        ("Save preferences", save_current_preferences),
        ("Load preferences", load_saved_preferences),
        ("Ask SmartBrew Assistant", open_assistant),
                ("Technician Dashboard", open_technician_dashboard),
        ("Recommend drinks", recommend_drinks),
        ("Save custom recipe", save_recipe),
        ("Load selected recipe", load_recipe),
        ("View order history", show_transaction_history),
        ("Order drink", order_drink),
    ]

    for index, (label, command) in enumerate(buttons):
        button = ttk.Button(
            button_frame,
            text=label,
            command=command,
        )
        button.grid(
            row=index // 3,
            column=index % 3,
            padx=4,
            pady=4,
            sticky="ew",
        )

    for column in range(3):
        button_frame.columnconfigure(column, weight=1)

    refresh_saved_recipes()
    preview_drink()


def main():
    """Initialize the database and display the login screen."""
    initialize_database()
    seed_inventory()

    root = tk.Tk()
    root.title("SmartBrew AI - Login")
    root.geometry("420x350")
    root.minsize(380, 320)

    title_label = ttk.Label(
        root,
        text="SmartBrew AI",
        font=("Arial", 22, "bold"),
    )
    title_label.pack(pady=(20, 5))

    subtitle_label = ttk.Label(
        root,
        text="Log in or create an account",
    )
    subtitle_label.pack(pady=(0, 15))

    login_frame = ttk.Frame(root, padding=10)
    login_frame.pack(fill="x", padx=20)

    ttk.Label(login_frame, text="Username:").grid(
        row=0, column=0, sticky="w", padx=5, pady=7
    )

    username_var = tk.StringVar()
    username_entry = ttk.Entry(
        login_frame,
        textvariable=username_var,
        width=25,
    )
    username_entry.grid(row=0, column=1, padx=5, pady=7)

    ttk.Label(login_frame, text="Password:").grid(
        row=1, column=0, sticky="w", padx=5, pady=7
    )

    password_var = tk.StringVar()
    password_entry = ttk.Entry(
        login_frame,
        textvariable=password_var,
        show="*",
        width=25,
    )
    password_entry.grid(row=1, column=1, padx=5, pady=7)

    def register():
        """Create a new user account using the entered credentials."""
        username = username_var.get().strip()
        password = password_var.get()

        try:
            success, message = create_account(username, password)

            if success:
                messagebox.showinfo(
                    "Account created",
                    f"{message}\nYou can now log in.",
                )
                password_var.set("")
            else:
                messagebox.showwarning("Registration failed", message)
        except Exception as error:
            messagebox.showerror(
                "Registration error",
                f"Could not create account:\n{error}",
            )

    def login():
        """Authenticate the entered credentials and open the main interface."""
        username = username_var.get().strip()
        password = password_var.get()

        try:
            user_id = authenticate_user(username, password)

            if user_id is None:
                messagebox.showerror(
                    "Login failed",
                    "Incorrect username or password.",
                )
                return

            show_main_window(root, user_id)
        except Exception as error:
            messagebox.showerror(
                "Login error",
                f"Could not log in:\n{error}",
            )

    login_button_frame = ttk.Frame(root, padding=5)
    login_button_frame.pack(pady=10)

    ttk.Button(
        login_button_frame,
        text="Log in",
        command=login,
        width=15,
    ).grid(row=0, column=0, padx=5)

    ttk.Button(
        login_button_frame,
        text="Create account",
        command=register,
        width=15,
    ).grid(row=0, column=1, padx=5)

    password_entry.bind("<Return>", lambda event: login())
    username_entry.focus_set()

    root.mainloop()


if __name__ == "__main__":
    main()
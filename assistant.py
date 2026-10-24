
"""Provide a simple natural-language assistant for SmartBrew AI."""


def get_assistant_response(
    message,
    beverages,
    preferences=None,
    availability_checker=None,
):
    """Answer common questions about drinks and the SmartBrew application.

    Args:
        message: The user's question or request.
        beverages: Dictionary containing drink prices and ingredients.
        preferences: Optional dictionary of the user's saved preferences.
        availability_checker: Optional function that checks ingredient stock.

    Returns:
        A readable response to the user's request.
    """
    question = message.strip().lower()

    if not question:
        return "Please type a question about SmartBrew or its drinks."

    greetings = ("hello", "hi", "hey", "good morning", "good afternoon")

    if any(question == greeting or question.startswith(greeting + " ")
           for greeting in greetings):
        return (
            "Hello! I'm the SmartBrew assistant. You can ask me about "
            "drinks, prices, ingredients, availability, or your preferences."
        )

    if any(word in question for word in ("help", "what can you do")):
        return (
            "I can help you explore the menu, check drink prices and "
            "ingredients, check ingredient availability, and explain "
            "how to order. Try asking: 'How much is a latte?'"
        )

    if any(word in question for word in ("menu", "what drinks", "which drinks",
                                         "list drinks", "available drinks")):
        drink_lines = []

        for name, details in beverages.items():
            price = details["price"]
            drink_lines.append(f"{name}: {price:.2f}")

        return "Here is the drink menu:\n" + "\n".join(drink_lines)

    if any(word in question for word in ("preference", "preferences",
                                         "my settings", "what do i like")):
        if not preferences:
            return (
                "I couldn't find saved preferences. Use the Save preferences "
                "button to save your drink customization choices first."
            )

        return (
            "Your saved preferences are:\n"
            f"Coffee strength: {preferences.get('coffee_strength', 'Not set')}\n"
            f"Milk: {preferences.get('milk', 'Not set')}\n"
            f"Temperature: {preferences.get('temperature', 'Not set')}\n"
            f"Syrup: {preferences.get('syrup', 'Not set')}"
        )

    if any(word in question for word in ("recommend", "suggestion",
                                         "suggest a drink", "what should i")):
        if preferences:
            milk = preferences.get("milk", "Regular")
            strength = preferences.get("coffee_strength", "Medium")

            if strength == "Strong":
                suggestion = "Espresso or Americano"
            elif milk != "None":
                suggestion = "Latte or Cappuccino"
            else:
                suggestion = "Americano or Hot Chocolate"

            return (
                f"Based on your saved preferences, you could try "
                f"{suggestion}. Check ingredient availability before ordering."
            )

        return (
            "I can suggest a drink, but you haven't saved preferences yet. "
            "Save your preferences first for a more personalized suggestion."
        )

    if any(word in question for word in ("order", "purchase", "buy", "payment")):
        return (
            "To order, select a drink and customize it, then click Preview "
            "drink to check availability. Click Order drink to confirm the "
            "order. Payment is simulated; no real money is charged."
        )

    for name, details in beverages.items():
        drink_name = name.lower()

        if drink_name in question:
            if any(word in question for word in ("price", "cost", "how much",
                                                  "expensive")):
                return f"{name} costs {details['price']:.2f}."

            if any(word in question for word in ("ingredient", "contain",
                                                  "made of", "what is in")):
                ingredients = details.get("ingredients", {})
                ingredient_lines = [
                    f"{ingredient}: {quantity}"
                    for ingredient, quantity in ingredients.items()
                ]

                return (
                    f"The ingredients listed for {name} are:\n"
                    + "\n".join(ingredient_lines)
                )

            if any(word in question for word in ("available", "in stock",
                                                  "can i get")):
                if availability_checker is None:
                    return (
                        "I can't check stock right now. Use Preview drink "
                        "in the main window to check availability."
                    )

                try:
                    available, result_message = availability_checker(
                        details.get("ingredients", {})
                    )
                except Exception:
                    return (
                        "I couldn't check the inventory just now. "
                        "Please try Preview drink in the main window."
                    )

                if available:
                    return f"{name} is currently available to order."

                return f"{name} is currently unavailable. {result_message}"

            return (
                f"{name} costs {details['price']:.2f}. "
                "You can ask me about its ingredients or availability too."
            )

    return (
        "I'm not sure how to answer that yet. Try asking about the menu, "
        "a drink's price or ingredients, stock availability, your saved "
        "preferences, or how to order."
    )

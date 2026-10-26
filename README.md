# SmartBrew AI

## 1. Overview

SmartBrew AI is a Python desktop application for a smart coffee shop. It supports user accounts, drink customization, ingredient inventory, custom recipes, recommendations, an assistant, simulated payments, order history, and technician functions.

## 2. Requirements

- Python 3
- Tkinter for the graphical interface
- SQLite, accessed through Python's built-in `sqlite3` module

No third-party Python packages are required by the current source imports.

Verify your installation:

```powershell
python --version
python -m tkinter
```

The second command should open a small test window. Close it before launching the application.

## 3. Setup and launch

1. Clone or download the repository: https://github.com/silvanabanica-cmyk/SmartBrewAI
2. Open PowerShell in the repository directory.
3. Verify that Python and Tkinter are available.
4. Enter the Task B folder and start the application:

```powershell
cd .\Task_B
python main.py
```

The application initializes its SQLite tables and seeds initial inventory when it starts. The database file is named `smartbrew.db` and is created in the current working directory.

## 4. Feature demonstration checklist

Use the GUI to demonstrate these ten functionalities, confirming each workflow in the running application:

1. **User accounts:** Create an account and log in.
2. **Drink customization:** Select a beverage and change its available options.
3. **Ingredient availability:** Inspect stock and check whether ingredients are available.
4. **Custom recipes:** Save and view a custom recipe.
5. **Recommendations:** Open the recommendation feature and inspect its suggestions.
6. **Assistant:** Submit a question and inspect the response.
7. **Simulated payment:** Place an order and follow the payment and receipt flow.
8. **Order history:** View previous orders or transactions.
9. **Inventory management:** Inspect stock and demonstrate the available refill function.
10. **Technician functions:** Open the technician dashboard and demonstrate its available functions.

These are demonstration targets; confirm the exact navigation and functionality in the application before submission.

## 5. Running the tests

Run the following commands from the repository directory:

```powershell
cd .\Task_B
python -m unittest discover -v
```

Review the results and resolve any failing tests before submission.

## 6. Database

The application uses SQLite. Its startup routine initializes the tables and adds initial inventory entries for Coffee, Water, Milk, and Chocolate without overwriting existing stock.

The local `smartbrew.db` file is excluded from the repository. The application should create a database when launched, but verify the fresh-install workflow before relying on it on another computer.

## 7. Source code

The application code and tests are located in `Task_B/`:

- `Task_B/main.py`: Application entry point and graphical interface.
- `Task_B/accounts.py`: Account creation, password hashing, and authentication.
- `Task_B/assistant.py`: Assistant response functionality.
- `Task_B/database.py`: Database initialization and data operations.
- `Task_B/test_accounts.py`, `Task_B/test_database.py`, `Task_B/test_inventory.py`: Automated tests.

Source functions and methods include docstrings describing their purposes, parameters, and return values.

## 8. LLM documentation

Document the LLM model and version used for each assignment task in the accompanying assignment report or prompt transcript. Do not assume that the repository alone satisfies this requirement.
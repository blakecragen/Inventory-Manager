import dearpygui.dearpygui as dpg
from db_manager import IngredientDatabase
from unitconverter import UnitConverter
import difflib

db = IngredientDatabase()

# === Callback Functions ===
def add_ingredient_callback():
    name = dpg.get_value("name_input").strip().title()
    amount = dpg.get_value("amount_input").strip()

    if not name or not amount:
        dpg.set_value("status_text", "⚠️ Ingredient name and amount required.")
        return

    db.add_ingredient(name, amount)
    dpg.set_value("status_text", f"✅ Added: {name}")
    refresh_list()

def delete_selected_callback():
    selected = dpg.get_value("ingredient_listbox")
    if selected:
        ingredient_id = int(selected[0].split(":")[0])
        db.delete_ingredient(ingredient_id)
        dpg.set_value("status_text", f"🗑️ Deleted ID: {ingredient_id}")
        refresh_list()

def update_amount_callback():
    selected = dpg.get_value("ingredient_listbox")
    new_amount = dpg.get_value("new_amount_input").strip()
    if selected and new_amount:
        ingredient_id = int(selected[0].split(":")[0])
        db.update_ingredient_amount(ingredient_id, new_amount)
        dpg.set_value("status_text", f"✅ Updated ID {ingredient_id} amount to {new_amount}")
        refresh_list()

def modify_amount_callback(mode):
    selected = dpg.get_value("ingredient_listbox")
    change_amount = dpg.get_value("change_amount_input").strip()
    if selected and change_amount:
        ingredient_id = int(selected[0].split(":")[0])
        current_amount = db.get_ingredient_amount(ingredient_id)
        try:
            if mode == "add":
                new_amount = UnitConverter.add(current_amount, change_amount)
            else:
                new_amount = UnitConverter.subtract(current_amount, change_amount)
            db.update_ingredient_amount(ingredient_id, new_amount)
            dpg.set_value("status_text", f"{mode.title()}ed {change_amount}. New amount: {new_amount}")
            refresh_list()
        except ValueError as e:
            dpg.set_value("status_text", f"❌ {str(e)}")

def search_callback():
    query = dpg.get_value("search_input").strip().lower()
    if not query:
        refresh_list()
        return

    matches = []
    for row in db.list_ingredients():
        name = row[1].lower()
        similarity = difflib.SequenceMatcher(None, query, name).ratio()
        if query in name or similarity > 0.6:
            matches.append(f"{row[0]}: {row[1]} ({row[2]})")

    dpg.configure_item("ingredient_listbox", items=matches)
    dpg.set_value("status_text", f"🔍 Found {len(matches)} match(es)")

def refresh_list():
    dpg.configure_item("ingredient_listbox", items=[
        f"{i[0]}: {i[1]} ({i[2]})" for i in db.list_ingredients()
    ])

# === GUI Layout ===
dpg.create_context()
dpg.create_viewport(title='Ingredient Manager', width=600, height=600)

with dpg.window(label="Inventory Interface", tag="main_window", width=580, height=580):

    dpg.add_text("Ingredient Name:")
    dpg.add_input_text(tag="name_input")

    dpg.add_text("Amount (e.g., 2 cups, 100 g):")
    dpg.add_input_text(tag="amount_input", width=200)

    dpg.add_button(label="Add Ingredient", callback=add_ingredient_callback)
    dpg.add_button(label="Delete Selected", callback=delete_selected_callback)

    dpg.add_spacer(height=5)
    dpg.add_input_text(tag="new_amount_input", label="New Amount")
    dpg.add_button(label="Update Amount", callback=update_amount_callback)

    dpg.add_spacer(height=5)
    dpg.add_input_text(tag="change_amount_input", label="Change Amount (Add/Subtract)")
    dpg.add_button(label="Add Amount", callback=lambda: modify_amount_callback("add"))
    dpg.add_button(label="Subtract Amount", callback=lambda: modify_amount_callback("subtract"))

    dpg.add_spacer(height=5)
    dpg.add_input_text(tag="search_input", label="Search Ingredient")
    dpg.add_button(label="Search", callback=search_callback)
    dpg.add_button(label="Refresh List", callback=refresh_list)

    dpg.add_listbox([], tag="ingredient_listbox", num_items=10, width=550)
    dpg.add_text("", tag="status_text", color=[200, 200, 0])

dpg.set_primary_window("main_window", True)
refresh_list()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

import sqlite3

class IngredientDatabase:
    def __init__(self, db_name="ingredients.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_ingredient(self, name, amount):
        self.cursor.execute('''
            INSERT INTO ingredients (name, amount)
            VALUES (?, ?)
        ''', (name, amount))
        self.conn.commit()

    def delete_ingredient(self, ingredient_id):
        self.cursor.execute('''
            DELETE FROM ingredients
            WHERE id = ?
        ''', (ingredient_id,))
        self.conn.commit()

    def update_ingredient_amount(self, ingredient_id, new_amount):
        self.cursor.execute('''
            SELECT name FROM ingredients WHERE id = ?
        ''', (ingredient_id,))
        result = self.cursor.fetchone()
        if result:
            name = result[0]
            self.cursor.execute('''
                UPDATE ingredients
                SET name = ?, amount = ?
                WHERE id = ?
            ''', (name, new_amount, ingredient_id))
            self.conn.commit()

    def get_ingredient_amount(self, ingredient_id):
        self.cursor.execute('SELECT amount FROM ingredients WHERE id = ?', (ingredient_id,))
        result = self.cursor.fetchone()
        return result[0] if result else ""

    def list_ingredients(self):
        self.cursor.execute('SELECT * FROM ingredients ORDER BY id')
        ingredients = self.cursor.fetchall()

        for new_id, row in enumerate(ingredients, start=1):
            old_id = row[0]
            self.cursor.execute('UPDATE ingredients SET id = ? WHERE id = ?', (new_id, old_id))

        self.conn.commit()

        self.cursor.execute('SELECT * FROM ingredients ORDER BY id')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

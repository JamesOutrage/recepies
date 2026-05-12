import sqlite3

DB_NAME = 'recipes.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instruction TEXT NOT NULL,
            time INTEGER DEFAULT 30,
            difficulty TEXT DEFAULT 'средняя',
            rating REAL DEFAULT 0,
            rating_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER,
            author TEXT,
            text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_recipes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, title, time, difficulty, rating FROM recipes ORDER BY created_at DESC')
    recipes = c.fetchall()
    conn.close()
    return recipes

def search_recipes(query):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT id, title, time, difficulty, rating 
        FROM recipes 
        WHERE title LIKE ? OR ingredients LIKE ?
        ORDER BY created_at DESC
    ''', (f'%{query}%', f'%{query}%'))
    recipes = c.fetchall()
    conn.close()
    return recipes

def get_recipe(recipe_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
    recipe = c.fetchone()
    
    c.execute('SELECT author, text, created_at FROM comments WHERE recipe_id = ? ORDER BY created_at DESC', (recipe_id,))
    comments = c.fetchall()
    conn.close()
    return recipe, comments

def add_recipe(title, ingredients, instruction, time, difficulty):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO recipes (title, ingredients, instruction, time, difficulty)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, ingredients, instruction, time, difficulty))
    conn.commit()
    conn.close()

def delete_recipe(recipe_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    conn.commit()
    conn.close()

def add_comment(recipe_id, author, text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO comments (recipe_id, author, text) VALUES (?, ?, ?)', 
              (recipe_id, author, text))
    conn.commit()
    conn.close()

def rate_recipe(recipe_id, rating):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT rating, rating_count FROM recipes WHERE id = ?', (recipe_id,))
    current_rating, count = c.fetchone()
    
    new_count = count + 1
    new_rating = ((current_rating * count) + rating) / new_count
    
    c.execute('UPDATE recipes SET rating=?, rating_count=? WHERE id=?', 
              (new_rating, new_count, recipe_id))
    conn.commit()
    conn.close()
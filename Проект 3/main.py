from flask import Flask, render_template, request, redirect, url_for, jsonify
import db as db
import random

app = Flask(__name__)
db.init_db()

@app.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        recipes = db.search_recipes(search)
    else:
        recipes = db.get_all_recipes()
    return render_template('index.html', recipes=recipes, search=search)

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe, comments = db.get_recipe(recipe_id)
    if not recipe:
        return "Рецепт не найден", 404
    return render_template('recipe.html', recipe=recipe, comments=comments)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        db.add_recipe(
            request.form['title'],
            request.form['ingredients'],
            request.form['instruction'],
            int(request.form['time']),
            request.form['difficulty']
        )
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    db.delete_recipe(recipe_id)
    return redirect(url_for('index'))

@app.route('/comment/<int:recipe_id>', methods=['POST'])
def add_comment(recipe_id):
    author = request.form.get('author', 'Аноним')
    text = request.form['text']
    if text:
        db.add_comment(recipe_id, author, text)
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/rate/<int:recipe_id>', methods=['POST'])
def rate_recipe(recipe_id):
    rating = int(request.form['rating'])
    if 1 <= rating <= 5:
        db.rate_recipe(recipe_id, rating)
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/api/random')
def api_random():
    recipes = db.get_all_recipes()
    if not recipes:
        return jsonify({'error': 'В книге пока нет рецептов'}), 404
    
    random_id = random.choice(recipes)[0]
    recipe, comments = db.get_recipe(random_id)
    
    return jsonify({
        'success': True,
        'recipe': {
            'id': recipe[0],
            'title': recipe[1],
            'ingredients': recipe[2],
            'instruction': recipe[3],
            'time': recipe[4],
            'difficulty': recipe[5],
            'rating': round(recipe[6], 1),
            'rating_count': recipe[7],
            'created_at': recipe[8]
        },
        'comments_count': len(comments)
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
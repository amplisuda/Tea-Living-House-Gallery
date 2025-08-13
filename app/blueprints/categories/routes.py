from flask import Blueprint, render_template
#from ...models import Image

categories_bp = Blueprint('categories', __name__, template_folder='templates')

@categories_bp.route('/<category>')
def category(category):
    #images = Image.query.filter_by(category=category).all()
    return render_template('categories/category.html', images=images, category=category)
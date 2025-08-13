from flask import Blueprint, render_template
#from ...models import Image

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')

@main_bp.route('/gallery')
def gallery():
    #images = Image.query.all()
    return render_template('main/gallery.html', images=images)

@main_bp.route('/search')
def search():
    #query = request.args.get('q', '')
    #images = Image.query.filter(Image.title.contains(query)).all()
    return render_template('main/search_results.html', images=images)
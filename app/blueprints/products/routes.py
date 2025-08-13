from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/contact_group')
def contact_group():
    return render_template('products/contact_group.html')


@products_bp.route('/product/<int:product_id>')
def product(product_id):
    return render_template('main/product_cart.html', images=images)
from flask import Blueprint, render_template
from ...models import Product
import json

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/contact_group')
def contact_group():
    return render_template('products/contact_group.html')


@products_bp.route('/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    product.image_url = json.loads(product.image_url)
    return render_template('main/product_cart.html', product=product)

@products_bp.route('/gallery')
def gallery():
    all_products = Product.query.order_by(Product.id.desc()).all()
    for product in all_products:
        product.image_url = json.loads(product.image_url)
    return render_template('main/gallery.html', products=all_products)

from flask import Blueprint, render_template
from ...models import Product
import json

products_bp = Blueprint('product', __name__, template_folder='templates')

@products_bp.route('/<string:hash>')
def product(hash):
    product = Product.query.filter_by(hash=hash).first()
    try:
        product.image_url = json.loads(product.image_url)
    except json.JSONDecodeError:
        print(500, description="Invalid image_url format")
    return render_template('main/product_cart.html', product=product)
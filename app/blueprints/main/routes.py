from flask import Blueprint, render_template, redirect, url_for, request
from ...models import Product
from random import choice
import json
from math import ceil

main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route('/')
def index():
    random_product = choice(Product.query.all()) if Product.query.count() > 0 else None
    random_product.image_url = json.loads(random_product.image_url)
    return render_template('main/index.html', random_product=random_product)


@main_bp.route('/<path:path>')
def redirect_index(path):
    return redirect(url_for('main.index'))


@main_bp.route('/about')
def about():
    return render_template('main/about.html')


@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')


@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    product = Product.query.filter(Product.description.contains(query)).all()
    return render_template('main/search_results.html', product=product)


PER_PAGE = 28

@main_bp.route('/gallery')
def gallery():
    page = int(request.args.get("page", 1))
    all_products = Product.query.order_by(Product.id.desc()).all()
    total_pages = max(1, ceil(len(all_products) / PER_PAGE))
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    products_page = all_products[start:end]
    for product in products_page:
        product.image_url = json.loads(product.image_url)
    return render_template(
        "main/gallery.html",
        products_page=products_page,
        page=page,
        total_pages=total_pages
    )


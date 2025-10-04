from flask import Blueprint, render_template, redirect, url_for, request
from ...models import Product, Category
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


PER_PAGE = 28


@main_bp.route('/gallery')
def gallery():
    page = int(request.args.get("page", 1))
    raw_category = request.args.get("category_id", None)  # сохраняем оригинал для строки

    categories = Category.query.order_by(Category.name).all() if hasattr(Product, 'category_id') else []
    category_tree = []
    category_map = {c.id: {'id': c.id, 'name': c.name, 'children': []} for c in categories}

    for category in categories:
        if category.parent_id is None:
            category_tree.append(category_map[category.id])
        else:
            if category.parent_id in category_map:
                category_map[category.parent_id]['children'].append(category_map[category.id])

    # Строим запрос
    query = Product.query.order_by(Product.id.desc())

    # Будем держать две переменные:
    # - category_id_int для фильтра
    # - selected_category_str для шаблона
    selected_category_str = "all"
    if raw_category and raw_category != "all":
        try:
            category_id_int = int(raw_category)
            subcategory_ids = [c.id for c in categories if c.parent_id == category_id_int]
            subcategory_ids.append(category_id_int)
            query = query.filter(Product.category_id.in_(subcategory_ids))
            selected_category_str = str(category_id_int)  # << ВАЖНО: строка для шаблона
        except ValueError:
            selected_category_str = "all"
    else:
        selected_category_str = "all"

    all_products = query.all()
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
        total_pages=total_pages,
        category_tree=category_tree,
        selected_category=selected_category_str,  # << всегда строка
    )



@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        products = []
    else:
        products = Product.query.filter(Product.description.ilike(f"%{query}%")).all()
    return render_template('main/gallery.html', products_page=products)

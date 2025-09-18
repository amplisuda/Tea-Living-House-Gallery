import vk_api
from datetime import datetime
from app import create_app
from app.models import db, Image
from app.config import Config
from sqlalchemy.sql import text


def load_vk_photos():
    app = create_app()

    vk_session = vk_api.VkApi(token=Config.VK_API_TOKEN)
    vk = vk_session.get_api()
    owner_id = -53195527
    album_id = 256927728
    count = 1000
    offset = 0

    with app.app_context():
        while True:
            try:
                response = vk.photos.get(
                    owner_id=owner_id,
                    album_id=album_id,
                    rev=0,
                    extended=0,
                    photo_sizes=1,
                    offset=offset,
                    count=count
                )

                for item in response['items']:
                    max_size = max(item['sizes'], key=lambda x: x['width'] * x['height'])
                    photo_url = max_size['url']
                    vk_id = str(item['id'])

                    if not Image.query.filter_by(vk_id=vk_id).first():
                        image = Image(
                            vk_id=vk_id,
                            title=item.get('text', ''),
                            url=photo_url,
                            category='uncategorized',
                            upload_date=datetime.fromtimestamp(item.get('date', 0))
                        )
                        db.session.add(image)

                db.session.commit()

                if len(response['items']) < count:
                    break

                offset += count

            except vk_api.exceptions.ApiError as e:
                print(f"VK API error: {e}")
                break
            except Exception as e:
                print(f"Error: {e}")
                db.session.rollback()
                break

def map_products():
    app = create_app()
    with app.app_context():
        try:
            db.session.execute(text("SELECT products_mapping();"))  # Функция для обработки товаров
            db.session.commit()
        except Exception as e:
            print(f"Error in map_products: {e}")
            db.session.rollback()

def update_categories():
    app = create_app()
    with app.app_context():
        try:
            db.session.execute(text("SELECT calc_categories();"))  # Функция категоризации товаров
            db.session.commit()
        except Exception as e:
            print(f"Error in update_categories: {e}")
            db.session.rollback()

if __name__ == '__main__':
    load_vk_photos()
    map_products()
    update_categories()
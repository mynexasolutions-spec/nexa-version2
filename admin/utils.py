import re
from models import BlogPost
from extensions import db

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def generate_unique_slug(title, post_id=None):
    base_slug = slugify(title)
    slug = base_slug
    counter = 1

    while True:
        query = BlogPost.query.filter_by(slug=slug)
        if post_id:
            query = query.filter(BlogPost.id != post_id)

        if not query.first():
            break

        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

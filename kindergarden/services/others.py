from slugify import slugify
import unicodedata


def get_new_slug(instance, instance_slug_field, title, session):
    new_slug = slugify(title.encode('utf-8'), to_lower=True)
    title_field = getattr(instance.__class__, instance_slug_field)

    res = session.query(instance.__class__).filter(title_field == title).order_by(instance.id).count()

    if res == 0:
        new_slug = new_slug
    else:
        new_slug = "%s-%s" % (new_slug, res + 1)

    return new_slug

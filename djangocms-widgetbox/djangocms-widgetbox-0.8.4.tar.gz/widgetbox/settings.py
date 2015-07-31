from django.conf import settings


GALLERY_STYLES = getattr(
    settings, 'WIDGETBOX_GALLERY_STYLES',
    (('widgetbox/gallery.html', 'default'),)
)

FAQ_STYLES = getattr(
    settings, 'WIDGETBOX_FAQ_STYLES',
    (('widgetbox/faq-topic.html', 'default'),)
)

DIVIDER_SIZES = getattr(
    settings, 'WIDGETBOX_DIVIDER_SIZES', ())

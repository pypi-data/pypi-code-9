from setuptools import setup

setup(
    name='django-lightweight-queue',
    version=1,
    packages=(
        'django_lightweight_queue',
        'django_lightweight_queue.management',
        'django_lightweight_queue.management.commands',
    )
)

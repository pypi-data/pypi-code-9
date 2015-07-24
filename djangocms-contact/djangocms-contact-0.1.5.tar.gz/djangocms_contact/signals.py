from django.dispatch import Signal

contact_new_message = Signal(providing_args=['name', 'email', 'subject', 'message'])

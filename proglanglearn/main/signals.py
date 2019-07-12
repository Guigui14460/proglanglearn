from django.dispatch import Signal


comment_signal = Signal(providing_args=['instance', 'request'])

user_logged_in = Signal(providing_args=['request'])

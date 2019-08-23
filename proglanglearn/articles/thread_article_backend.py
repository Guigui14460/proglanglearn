from threading import Thread, RLock

from .models import Article
from .utils import send_email_new_article


lock = RLock()


class SendEmailArticle(Thread):
    def __init__(self, request):
        Thread.__init__(self)
        self.request = request

    def run(self):
        with lock:
            article_email_to_send = Article.objects.get_send_email_article()
            for article in article_email_to_send:
                send_email_new_article(self.request, article)
            article_email_to_send.update(email_send=True)

from threading import Thread, RLock

from .models import Course
from .utils import send_email_new_course


lock = RLock()


class SendEmailCourse(Thread):
    def __init__(self, request):
        Thread.__init__(self)
        self.request = request

    def run(self):
        with lock:
            course_email_to_send = Course.objects.get_send_email_course()
            for course in course_email_to_send:
                send_email_new_course(self.request, course)
            course_email_to_send.update(email_send=True)

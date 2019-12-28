import datetime
from threading import Thread, RLock

from django.utils.timezone import now, timedelta

from analytics.models import UserExperienceJournal
from polls.models import Poll
from .models import EmailAdminNotificationForUsers, IndexBanner


lock = RLock()


class DeleteUselessData(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        with lock:
            now_ = now()
            today = datetime.date.today()
            user_exp_journal_qs = UserExperienceJournal.objects.filter(
                timestamp__lte=now_ - timedelta(days=8))
            if user_exp_journal_qs.exists():
                for journal in user_exp_journal_qs:
                    journal.delete()
            email_admin = EmailAdminNotificationForUsers.objects.filter(
                timestamp__lte=now_ - timedelta(days=3), is_sent=True)
            if email_admin.exists():
                for email in email_admin:
                    email.delete()
            poll_ended = Poll.objects.filter(end_date__lte=today)
            if poll_ended.exists():
                for poll in poll_ended:
                    for user_vote in poll.user_votes.all():
                        user_vote.delete()
            
            ib_qs = IndexBanner.objects.filter(end_time__lte=now_ + timedelta(days=7))
            if ib_qs.exists():
                for banner in ib_qs:
                    banner.delete()

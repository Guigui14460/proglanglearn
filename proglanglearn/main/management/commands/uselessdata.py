from django.core.management.base import BaseCommand, CommandError

from main.thread_remove_useless_info import DeleteUselessData


class Command(BaseCommand):
    help = "Delete useless data"

    def handle(self, *args, **options):
        try:
            thread = DeleteUselessData()
            thread.start()
        except:
            raise CommandError("Objects not exist")
        self.stdout.write(self.style.SUCCESS(
            "Useless data succesfully deleted"))

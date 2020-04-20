from django.core.management.base import BaseCommand, CommandError
from banner_detector.tasks import recalculate_base_banners_descriptors, parse_buses


class Command(BaseCommand):
    help = "Upload into database all buses from buses.csv "

    def handle(self, *args, **options):
        """
        Method load buses into database
        :param args:
        :param options:
        :return:
        """
        try:
            parse_buses()
        except Exception as e:
            raise CommandError('Bus parsing error "%s"' % e)

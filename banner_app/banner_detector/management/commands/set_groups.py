from django.core.management.base import BaseCommand, CommandError
from banner_detector.tasks import recalculate_base_banners_descriptors, parse_buses


class Command(BaseCommand):
    """
    management command for descriptors updating
    """
    help = "Recalculate all descriptors in database"

    def handle(self, *args, **options):
        """
        Method recalculate all descriptors in database
        Start only if recognition model was updated
        :param args:
        :param options:
        :return:
        """
        try:
            parse_buses()
        except Exception as e:
            raise CommandError('set groups error "%s"' % e)

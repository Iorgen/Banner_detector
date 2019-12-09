from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.conf import settings


class Command(BaseCommand):
    """
    management command setting base groups
    """
    help = "Set manager and worker groups"

    def handle(self, *args, **options):
        """
        Method set all start groups, start after new place deployed
        :param args:
        :param options:
        :return:
        """
        try:
            manager_role, manager_created = Group.objects.get_or_create(name='manager')
            if manager_created:
                manager_role.permissions.add(Permission.objects.all())
            worker_role, worker_created = Group.objects.get_or_create(name='worker')
            if worker_created:
                worker_role.permissions.add(Permission.objects.get(codename='add_billboard'))

        except Exception as e:
            raise CommandError('set groups error "%s"' % e)

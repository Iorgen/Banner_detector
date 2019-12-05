from django.db import models


class BannerQuerySet(models.QuerySet):
    def non_recognized(self):
        return self.filter(recognition_status=False)

    def unknown(self):
        return self.filter(recognition_status=True, banner_object__banner_type=None)

    def recognized_by_billboard_id_quantity(self, billboard_id):
        pass


class BannerManager(models.Manager):
    def get_queryset(self):
        return BannerQuerySet(self.model, using=self._db)

    def non_recognized(self):
        return self.get_queryset().non_recognized()

    def unknown(self):
        return self.get_queryset().unknown()

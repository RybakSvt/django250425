from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from library.models import Category


@receiver(signal=post_save, sender=Category)
def category_saved(sender, instance, created, **kwargs):
    if created:
        print(f"New category was created: Category name: {instance.name_category} ")
    else:
        print(f"The category was update: Category name: {instance.name_category} ")


# def category_saved(sender, instance, created, **kwargs):
#     if created:
#         print(f"New category was created: Category name: {instance.name_category} ")
#     else:
#         print(f"The category was update: Category name: {instance.name_category} ")
#
# post_save.connect(category_saved, sender=Category)






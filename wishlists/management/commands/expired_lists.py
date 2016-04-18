
from wishlists.models import List
from django.core.management import BaseCommand
from django.utils import timezone
import stripe


def refund_pledge(item):
    '''
    Sripe API docs include good Refund instructions here:
     https://stripe.com/docs/api#refunds
    '''

    for pledge in item.pledges:
        re = stripe.Refund.create(charge=pledge.charge_id)

class Command(BaseCommand):
    '''

    Expired lists are the lists whose deadline has passed. To prevent
    embezzlement, all pledges for items that have not been fully funded
    prior to the list's deadline will be refunded to the donor.

    '''

    def handle(self, *args, **options):

        present_day = timezone.now().date()

        expired_lists_qs = List.ojbjects.filter(expired=True)\
            .filter(deadline__lte=present_day)

        for expired_list in expired_lists_qs:
            expired_list.expired = True

            for item in expired_list.items:
                if not item.funded_item:
                    refund_pledge(item)


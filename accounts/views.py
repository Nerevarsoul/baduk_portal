from datetime import date

from django.db.models import Prefetch
from django.views.generic import ListView

from accounts.models import User, Subscription


class TsumegoAddSolutionView(ListView):
    template_name = 'user_subscriptions_list.html'

    def get_queryset(self):
        year = self.kwargs.get('year', date.today().year)
        month = self.kwargs.get('month', date.today().month)

        return User.objects.prefetch_related(
            Prefetch(
                'subscriptions',
                queryset=Subscription.objects.get_subscriptions_by_date(year, month),
                to_attr='active_subscriptiions'
            )
        )

import django_filters
from .models import Record


class RecordFilter(django_filters.FilterSet):
    # these let you filter by date range, like ?start_date=2024-01-01&end_date=2024-06-30
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Record
        fields = ['category', 'transaction_type', 'start_date', 'end_date']

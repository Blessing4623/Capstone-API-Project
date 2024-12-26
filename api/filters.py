import django_filters
from .models import Review
# defining a filter for the review ratings since it is under movie view set
class ReviewFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter()
    class Meta:
        model = Review
        fields = ['rating']
import django_filters

from core.models import Profile


class ProfileFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['search_query']

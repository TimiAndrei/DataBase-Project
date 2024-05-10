from django import template

register = template.Library()

@register.inclusion_tag('fragments/pagination.html')
def render_pagination(queryset, request):
    paginator = queryset.paginator
    page_obj = queryset
    return {'paginator': paginator, 'page_obj': page_obj, 'request': request}
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def get_pagination_context(page_obj, per_page=10):
    return {
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_range': page_obj.paginator.get_elided_page_range(page_obj.number, on_each_side=3, on_ends=2),
    }
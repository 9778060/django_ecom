from django import template

register = template.Library()

@register.filter
def filter_order_item_by_order_id(order_items, id_):
    return order_items.filter(order_id=id_)

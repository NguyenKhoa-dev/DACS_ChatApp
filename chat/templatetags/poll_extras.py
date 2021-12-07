from django import template

register = template.Library()

@register.filter(name='test_cut')
def test_cut(value, arg):
    return value>arg

@register.filter(name="user_filter")
def user_filter(rhs,room):
    rhs1 = rhs.filter(room=room)
    users = [rh.user for rh in rhs1]
    return users

@register.filter(name="user_compare")
def user_compare(users,user):
    return user in users
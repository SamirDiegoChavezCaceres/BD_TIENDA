from django import template

register = template.Library() 
#https://stackoverflow.com/questions/34571880/how-to-check-in-template-if-user-belongs-to-a-group
@register.filter(name='belongs_to') 
def belongs_to(user, group_name):
    return user.groups.filter(name=group_name).exists() 
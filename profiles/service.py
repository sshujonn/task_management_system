from menu.models import Menu
from parent_menu.models import ParentMenu
from profiles.serializers import MenuSerializer


class ProfileService:

    def get_menu(self, user):
        groups = user.groups.all()
        menus = Menu.objects.filter(group__in=groups)
        result = {}
        for menu in menus:
            p_menu_name = menu.parent_menu.p_menu_name
            if not result.get(p_menu_name):
                result[p_menu_name] = []
                if {'menu_name':menu.menu_name, 'url': menu.related_url} not in result.get(p_menu_name):
                    result[p_menu_name].append({'menu_name':menu.menu_name, 'url': menu.related_url})
            else:
                if {'menu_name':menu.menu_name, 'url': menu.related_url} not in result.get(p_menu_name):
                    result[p_menu_name].append({'menu_name':menu.menu_name, 'url': menu.related_url})
        return result

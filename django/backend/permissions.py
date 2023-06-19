from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class Permissions:

    def get_perms_on_login(self, request):
        try:
            group_objs = request.user.get_group_permissions()
            perm_obj = {}
            for perm in group_objs:
                perm_str = perm.split('.')[1]
                perm_data = perm_str.split('_')
                perm_type = perm_data[0]
                perm_module = perm_data[1]
                if perm_module not in perm_obj:
                    perm_obj[perm_module] = {perm_type: True}
                else:
                    perm_obj[perm_module][perm_type] = True
            return perm_obj
        except:
            return {}

    def get_perms_of_role(self, id):
        try:
            group_obj = Group.objects.get(id=id)
            group_objs = group_obj.permissions.all()
            all_permissions = Permission.objects.all()
            perm_obj = {}
            return_obj = {}
            for perm in all_permissions:
                perm_str = perm.codename
                perm_data = perm_str.split('_')
                perm_type = perm_data[0]
                perm_module = perm_data[1]
                if perm_module not in perm_obj:
                    perm_obj[perm_module] = {perm_type: False}
                else:
                    perm_obj[perm_module][perm_type] = False
            for perm in group_objs:
                perm_str = perm.codename
                perm_data = perm_str.split('_')
                perm_type = perm_data[0]
                perm_module = perm_data[1]
                if perm_module not in perm_obj:
                    perm_obj[perm_module] = {perm_type: True}
                else:
                    perm_obj[perm_module][perm_type] = True
            return_obj['permission'] = perm_obj
            return_obj['name'] = group_obj.name
            return_obj['id'] = group_obj.id
            return return_obj
        except Exception as err:
            return {}

    def update_role_data(self, id, updated_roles={}):
        try:
            group_obj = Group.objects.get(id=id)
            add_list = []
            remove_list = []
            for key in updated_roles:
                if (updated_roles[key]):
                    add_list.append(key)
                else:
                    remove_list.append(key)
            add_perm_obj = Permission.objects.filter(codename__in=add_list)
            remove_perm_obj = Permission.objects.filter(
                codename__in=remove_list)
            group_obj.permissions.add(*add_perm_obj)
            group_obj.permissions.remove(*remove_perm_obj)
            group_obj.save()
            return {'status': 'success'}
        except Exception as err:
            print('x')
            return {'status': 'error'}

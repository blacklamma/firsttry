

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

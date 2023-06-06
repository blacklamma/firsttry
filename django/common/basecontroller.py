

import json
import os
import base64
from backend.settings import FILE_PATH


class BaseController():
    noneList = [None, "None", u'None', "Null", "null", "", -1,
                "-1", "0", "Select", [], {}, (), ' ', u'', u' ', [''], [{}]]
    dbNoneList = ["None", "Null", "null", -
                  1, "-1", "Select",  {}, (), u'', u' ']

    def get_post_data(self, request, key="data"):
        data = json.loads(request.POST.get(key, "{}"))
        if not data:
            flag = 0
            key_list = request.POST.keys()
            if not key_list:
                key_list = request.data.keys()
                flag = 1
            if key_list:
                for item in key_list:
                    if flag == 1:
                        data[item] = request.data.get(item, '')
                    else:
                        data[item] = request.POST.get(item, '')
        return data

    def save_file(self, data, attachment_dir):
        try:
            file_path = self.get_file_attachment_path(attachment_dir)
            final_file_path = file_path + os.sep + data.get('name')
            if 'base64,' in data.get('data'):
                data['data'] = data.get('data').split('base64,')[1]
            with open(final_file_path, "wb") as fh:
                fh.write(base64.b64decode(data.get('data')))
            return final_file_path
        except Exception as err:
            return ''

    def get_file_attachment_path(self, attachment_dir):
        """
        :param organization_id: Every Organization will have seperate repository to store the file identified by this id
        :param ref_id: To store the seperate document for each Reference ID of the module
        :param module_name: Seperate path for each Module
        module_name --> Organization ID --> ref_id --> Zipfile & File name
        :return: It will return the file patch
        """
        try:
            file_path = str(FILE_PATH) + os.sep + "files" + \
                os.sep + attachment_dir
            if not os.path.isdir(file_path):
                os.makedirs(file_path)
            return file_path
        except Exception as e:
            return ''

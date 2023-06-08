import base64
import os
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from common.basecontroller import BaseController
from backend.permissions import Permissions
from .models import Customer, UserProfile
from .serializer import CustomerDataSerializer, CustomerListSerializer, UserListSerializer, UserDataSerializer, UserProfileDataSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator


def login_page(request):
    request_data = json.loads(request.body)
    username = request_data.get('username')
    password = request_data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        return_obj = {'msg': 'Login Successful', 'is_staff': user.is_staff}
        login(request, user)
        if user.is_staff:
            user_profile_obj = UserProfile.objects.get(user=user)
            return_obj['user_id'] = user.id
        else:
            user_profile_obj = Customer.objects.get(user=user)
            return_obj['cust_id'] = user_profile_obj.id
        image_path = user_profile_obj.profile_path
        image_data = ''
        if image_path:
            with open(image_path, "rb") as img_file:
                b64str = base64.b64encode(img_file.read())
            image_data = 'data:image/jpeg;base64,' + b64str.decode('utf-8')
            return_obj['profile_image'] = image_data
        perm_obj = Permissions()
        return_obj['permissions'] = perm_obj.get_perms_on_login(request)
        return JsonResponse(return_obj)
    else:
        return JsonResponse({'msg': 'Username OR password is incorrect'})


def logout_page(request):
    try:
        request_data = json.loads(request.body)
        username = request_data.get('username')

        user = User.objects.get(username=username)

        if user is not None:
            logout(request)
            return HttpResponse('Success!')
        else:
            return HttpResponse('Error!')
    except Exception as err:
        return HttpResponse('Error!')


class UserView(viewsets.ModelViewSet, BaseController):
    queryset = User.objects.filter(
        is_active=True, is_staff=True, is_superuser=False)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        try:
            init_filter = ~Q(id=request.user.id) & Q(is_staff=True)
            user_prof_ids = UserProfile.objects.filter(
                ~Q(is_deleted=True)).values_list('user_id', flat=True)
            init_filter &= Q(id__in=user_prof_ids)
            user_obj = User.objects.filter(init_filter)
            # Show 25 contacts per page.
            paginator = Paginator(user_obj, 25)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            serializer = UserListSerializer(page_obj, many=True)
            user_data = serializer.data
            final_data = [dict(x) for x in user_data]
            return JsonResponse(final_data, status=200, safe=False)
        except Exception as err:
            return JsonResponse([], status=200)

    def create(self, request):
        try:
            post_data = self.get_post_data(request)
            post_data['is_staff'] = True
            update_flag = False
            if post_data.get('id') not in self.noneList:
                update_flag = True
            user_obj = self.save_user_data(post_data, update_flag)
            self.save_user_profile_data(post_data, user_obj, update_flag)
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error'}, status=200)

    def retrieve(self, request, pk):
        try:
            user_obj = User.objects.get(id=pk)
            role_obj = user_obj.groups.all()
            role_id = None
            if role_obj:
                role_id = role_obj[0].id
            user_profile_obj = UserProfile.objects.get(user_id=pk)
            prof_serializer = UserProfileDataSerializer(user_profile_obj)
            serializer = UserDataSerializer(
                user_obj, context={'prof_data': prof_serializer.data, 'role_id': role_id})
            user_data = serializer.data
            return JsonResponse(dict(user_data), status=200)
        except Exception as err:
            return JsonResponse({}, status=200)

    def destroy(self, request, pk):
        try:
            UserProfile.objects.filter(user_id=pk).update(is_deleted=True)
            user_obj = User.objects.get(id=pk)
            user_obj.is_active = False
            temp_username = user_obj.username
            check_username = True
            while check_username:
                check_username = User.objects.filter(
                    username=temp_username+'_old').count()
                temp_username += '_old'
            user_obj.username = temp_username
            user_obj.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error'}, status=200)

    def save_user_data(self, data, update_flag=False):
        try:
            if update_flag:
                user_obj = User.objects.get(username=data.get('username', ''))
            else:
                user_obj = User()
            user_obj.username = data.get('username', '')
            if data.get('password') != '*****************':
                user_obj.set_password(data.get('password'))
            user_obj.first_name = data.get('first_name', '')
            user_obj.last_name = data.get('last_name', '')
            user_obj.email = data.get('email', '')
            user_obj.is_active = data.get('is_active', False)
            user_obj.is_staff = data.get('is_staff', False)
            if data.get('role_id'):
                user_obj.groups.add(data.get('role_id'))
            user_obj.save()
            return user_obj
        except Exception as err:
            return None

    def save_user_profile_data(self, data, user_obj, update_flag=False):
        try:
            file_path = ''
            if data.get('file'):
                file_path = self.save_file(
                    data.get('file'), 'profile' + os.sep + str(user_obj.id))
            if update_flag:
                user_prof_obj = UserProfile.objects.get(user=user_obj)
            else:
                user_prof_obj = UserProfile()
            user_prof_obj.user = user_obj
            user_prof_obj.department = data.get('department', '')
            user_prof_obj.designation = data.get('designation', '')
            user_prof_obj.contact_number = data.get('contact_number', '')
            user_prof_obj.contact_extension = data.get('contact_extension', '')
            if file_path not in self.noneList:
                user_prof_obj.profile_path = file_path
            user_prof_obj.save()
            return user_prof_obj
        except Exception as err:
            return None

    @action(detail=False, url_path='options')
    def get_options(self, request):
        try:
            options = {'role_options': []}
            # groups
            init_filter = ~Q(name__in=['Customer'])
            group_options = Group.objects.filter(init_filter)
            for group in group_options:
                options['role_options'].append(
                    {'id': group.id, 'name': group.name})
            return JsonResponse(options, status=200, safe=False)
        except Exception as err:
            return JsonResponse({}, status=200)


class CustomerView(viewsets.ModelViewSet, BaseController):
    queryset = Customer.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        try:
            init_filter = Q(is_deleted=False)
            requester_obj = Customer.objects.filter(init_filter)
            # Show 25 contacts per page.
            paginator = Paginator(requester_obj, 25)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            serializer = CustomerListSerializer(page_obj, many=True)
            user_data = serializer.data
            final_data = [dict(x) for x in user_data]
            return JsonResponse(final_data, status=200, safe=False)
        except Exception as err:
            return JsonResponse([], status=200)

    def create(self, request):
        try:
            post_data = self.get_post_data(request)
            post_data['is_staff'] = False
            update_flag = False
            if post_data.get('id') not in self.noneList:
                update_flag = True
            reponse = self.save_customer_data(post_data, update_flag)
            return JsonResponse(reponse, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error'}, status=200)

    def retrieve(self, request, pk):
        try:
            cust_obj = Customer.objects.get(id=pk)
            serializer = CustomerDataSerializer(cust_obj)
            cust_data = serializer.data
            return JsonResponse(dict(cust_data), status=200)
        except Exception as err:
            return JsonResponse({}, status=200)

    def destroy(self, request, pk):
        try:
            cust_obj = Customer.objects.get(id=pk)
            if cust_obj.login_enabled:
                user_id = cust_obj.user_id
                user_obj = User.objects.get(id=user_id)
                user_obj.is_active = False
                temp_username = user_obj.username
                check_username = True
                while check_username:
                    check_username = User.objects.filter(
                        username=temp_username+'_old').count()
                    temp_username += '_old'
                user_obj.username = temp_username
                user_obj.save()
            cust_obj.is_deleted = True
            cust_obj.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error'}, status=200)

    def save_user_data(self, data, update_flag=False):
        try:
            if update_flag:
                user_obj = User.objects.get(username=data.get('username', ''))
            else:
                user_obj = User()
            user_obj.username = data.get('username', '')
            if data.get('password') != '*****************':
                user_obj.set_password(data.get('password'))
            user_obj.first_name = data.get('customer_name', '')
            user_obj.last_name = data.get('customer_name', '')
            user_obj.email = data.get('email', '')
            user_obj.is_active = data.get('is_active', False)
            user_obj.is_staff = data.get('is_staff', False)
            user_obj.groups.add(4)
            user_obj.save()
            return user_obj
        except Exception as err:
            return None

    def save_customer_data(self, data, update_flag=False):
        try:
            if update_flag:
                cust_prof_obj = Customer.objects.get(id=data.get('id'))
            else:
                cust_prof_obj = Customer()
            cust_prof_obj.customer_name = data.get('customer_name', '')
            cust_prof_obj.login_enabled = data.get('login_enabled', False)
            if data.get('username', False):
                user_obj = self.save_user_data(data, update_flag)
                cust_prof_obj.user = user_obj
            cust_prof_obj.contact_number = data.get('contact_number', '')
            cust_prof_obj.email = data.get('email', '')
            file_path = ''
            if data.get('file'):
                file_path = self.save_file(
                    data.get('file'), 'cust' + os.sep + str(cust_prof_obj.id))
            if file_path not in self.noneList:
                cust_prof_obj.profile_path = file_path
            cust_prof_obj.save()
            return {'status': 'success'}
        except Exception as err:
            return {'status': 'error'}

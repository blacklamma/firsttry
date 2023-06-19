from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
import json
from django.core.paginator import Paginator

from common.basecontroller import BaseController
from .serializers import EmailToTicketConfSerializer, IncomingEmailsListSerializer, NotificationsListSerializer, OutgoingEmailsListSerializer, RulesListSerializer, SMTPSerializer, StatusListSerializer, WFListSerializer
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework import viewsets
from rest_framework.decorators import action


class EmailView(viewsets.ModelViewSet, BaseController):
    queryset = OutgoingEmails.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(detail=False, url_path='outEmails')
    def get_outgoing_emails_list(self, request):
        try:
            init_filter = Q(is_deleted=False)
            requester_obj = OutgoingEmails.objects.filter(init_filter)
            # Show 25 contacts per page.
            paginator = Paginator(requester_obj, 25)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            serializer = OutgoingEmailsListSerializer(page_obj, many=True)
            user_data = serializer.data
            final_data = [dict(x) for x in user_data]
            return JsonResponse(final_data, status=200, safe=False)
        except Exception as err:
            return JsonResponse({}, status=200)

    @action(detail=False, methods=['post'], url_path='saveOutConf')
    def save_outgoing_email_conf(self, request):
        try:
            post_data = self.get_post_data(request)
            if post_data.get('id') not in self.noneList:
                smtp_obj = SMTPConf.objects.get(
                    id=post_data.get('id'))
            else:
                smtp_obj = SMTPConf()
            smtp_obj.host_name = post_data.get('host_name', '')
            smtp_obj.host_username = post_data.get('host_username', '')
            if post_data.get('host_password') != '*****************':
                smtp_obj.host_password = post_data.get('host_password', '')
            smtp_obj.host_email = post_data.get('host_email', '')
            smtp_obj.host_port = post_data.get('host_port', '')
            smtp_obj.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error'}, status=200)

    @action(detail=False, methods=['get'], url_path='getOutConf')
    def get_outgoing_email_conf(self, request):
        try:
            init_filter = Q(is_deleted=False)
            outgoing_obj = SMTPConf.objects.filter(init_filter)
            if outgoing_obj:
                outgoing_obj = outgoing_obj[0]
                serializer = SMTPSerializer(outgoing_obj)
                outgoing_data = serializer.data
                return JsonResponse(dict(outgoing_data), status=200)
            else:
                return JsonResponse({}, status=200)
        except Exception as err:
            return JsonResponse({}, status=200)

    @action(detail=False, url_path='inEmails')
    def get_incoming_emails_list(self, request):
        try:
            init_filter = Q(is_deleted=False)
            incoming_obj = IncomingEmails.objects.filter(init_filter)
            # Show 25 contacts per page.
            paginator = Paginator(incoming_obj, 25)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            serializer = IncomingEmailsListSerializer(page_obj, many=True)
            user_data = serializer.data
            final_data = [dict(x) for x in user_data]
            return JsonResponse(final_data, status=200, safe=False)
        except Exception as err:
            return JsonResponse({}, status=200)

    @action(detail=False, methods=['post'], url_path='saveInConf')
    def save_incoming_email_conf(self, request):
        try:
            post_data = self.get_post_data(request)
            if post_data.get('id') not in self.noneList:
                email_to_ticket_obj = EmailToTicketConf.objects.get(
                    id=post_data.get('id'))
            else:
                email_to_ticket_obj = EmailToTicketConf()
            email_to_ticket_obj.email_server = post_data.get(
                'email_server', '')
            email_to_ticket_obj.smtp_host_port = post_data.get(
                'smtp_host_port', 993)
            email_to_ticket_obj.email_id = post_data.get('email_id', '')
            if post_data.get('password') != '*****************':
                email_to_ticket_obj.password = post_data.get('password', '')
            email_to_ticket_obj.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error'}, status=200)

    @action(detail=False, methods=['get'], url_path='getInConf')
    def get_incoming_email_conf(self, request):
        try:
            init_filter = Q(is_deleted=False)
            incoming_obj = EmailToTicketConf.objects.filter(init_filter)
            if incoming_obj:
                incoming_obj = incoming_obj[0]
                serializer = EmailToTicketConfSerializer(incoming_obj)
                incoming_data = serializer.data
                return JsonResponse(dict(incoming_data), status=200)
            else:
                return JsonResponse({}, status=200)
        except Exception as err:
            return JsonResponse({}, status=200)


class WorkflowView(viewsets.ModelViewSet, BaseController):
    queryset = Workflow.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        try:
            init_filter = Q(is_deleted=False)
            owner_map = {}
            wf_obj = Workflow.objects.filter(init_filter)
            # Show 25 contacts per page.
            paginator = Paginator(wf_obj, 25)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            wf_owner_obj = WorkflowOwners.objects.filter(
                init_filter).select_related('owner')
            for owner_obj in wf_owner_obj:
                owner_name = owner_obj.owner.first_name
                if owner_obj.owner.last_name not in self.noneList:
                    owner_name += ' ' + owner_obj.owner.last_name
                if owner_obj.wf_id not in owner_map:
                    owner_map[owner_obj.wf_id] = owner_name
                else:
                    owner_map[owner_obj.wf_id] += ', ' + owner_name
            serializer = WFListSerializer(
                page_obj, many=True, context={'owners': owner_map})
            user_data = serializer.data
            final_data = [dict(x) for x in user_data]
            return JsonResponse(final_data, status=200, safe=False)
        except Exception as err:
            return JsonResponse([], status=200)

    def create(self, request):
        try:
            post_data = self.get_post_data(request)
            if post_data.get('id') not in self.noneList:
                wf_obj = Workflow.objects.get(id=post_data.get('id'))
            else:
                wf_obj = Workflow()
            wf_obj.name = post_data.get('name')
            wf_obj.save()
            wf_id = wf_obj.id
            owner_list = post_data.get('owners')
            existing_owners = list(WorkflowOwners.objects.filter(
                wf_id=wf_id, is_deleted=False).values_list('owner_id', flat=True))
            ui_owners = self.get_ids_from_obj(owner_list)
            diff_list = [iter for iter in existing_owners +
                         ui_owners if iter not in existing_owners or iter not in ui_owners]
            del_list = []
            for user_id in diff_list:
                if user_id in ui_owners:
                    wf_owner_obj = WorkflowOwners()
                    wf_owner_obj.wf_id = wf_id
                    wf_owner_obj.owner_id = user_id
                    wf_owner_obj.save()
                elif user_id in existing_owners:
                    del_list.append(user_id)
            if del_list not in self.noneList:
                WorkflowOwners.objects.filter(
                    wf_id=wf_id, owner_id__in=del_list).update(is_deleted=True)
            return JsonResponse({'status': 'success', 'data': {'id': wf_id}}, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error', 'data': {}}, status=200)

    def retrieve(self, request, pk):
        try:
            wf_data = {}
            owner_list = []
            wf_obj = Workflow.objects.get(id=pk)
            wf_data['id'] = wf_obj.id
            wf_data['name'] = wf_obj.name
            existing_owners = WorkflowOwners.objects.filter(wf_id=wf_obj.id, is_deleted=False).values(
                'owner_id', 'owner__first_name', 'owner__last_name')
            for owner in existing_owners:
                owner_name = owner.get('owner__first_name')
                if owner.get('owner__last_name') not in self.noneList:
                    owner_name += ' ' + owner.get('owner__last_name')
                owner_list.append(
                    {'id': owner.get('owner_id'), 'name': owner_name})
            wf_data['owners'] = owner_list
            return JsonResponse(wf_data, status=200)
        except Exception as err:
            return JsonResponse({}, status=200)

    def destroy(self, request, pk):
        try:
            print('x')
            # cust_obj = Customer.objects.get(id=pk)
            # if cust_obj.login_enabled:
            #     user_id = cust_obj.user_id
            #     user_obj = User.objects.get(id=user_id)
            #     user_obj.is_active = False
            #     temp_username = user_obj.username
            #     check_username = True
            #     while check_username:
            #         check_username = User.objects.filter(
            #             username=temp_username+'_old').count()
            #         temp_username += '_old'
            #     user_obj.username = temp_username
            #     user_obj.save()
            # cust_obj.is_deleted = True
            # cust_obj.save()
            # return JsonResponse({'status': 'success'}, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error'}, status=200)

    def save_user_data(self, data, update_flag=False):
        try:
            print('x')
            # if update_flag:
            #     user_obj = User.objects.get(username=data.get('username', ''))
            # else:
            #     user_obj = User()
            # user_obj.username = data.get('username', '')
            # if data.get('password') != '*****************':
            #     user_obj.set_password(data.get('password'))
            # user_obj.first_name = data.get('customer_name', '')
            # user_obj.last_name = data.get('customer_name', '')
            # user_obj.email = data.get('email', '')
            # user_obj.is_active = data.get('is_active', False)
            # user_obj.is_staff = data.get('is_staff', False)
            # user_obj.groups.add(4)
            # user_obj.save()
            # return user_obj
        except Exception as err:
            return None

    @action(detail=False, url_path='options/(?P<wf_id>[^/]+)')
    def get_options(self, request, wf_id=None):
        try:
            wf_filter = Q()
            options = {'owner_options': [],
                       'state_options': [], 'status_options': []}
            user_options = User.objects.filter(is_staff=True, is_active=True)
            for user in user_options:
                options['owner_options'].append(
                    {'id': user.id, 'name': user.get_full_name()})
            state_options = State.objects.filter(is_deleted=False)
            for state in state_options:
                options['state_options'].append(
                    {'id': state.id, 'name': state.name})
            if wf_id not in self.noneList:
                wf_filter = Q(wf_id=wf_id)
            status_options = Status.objects.filter(wf_filter, is_deleted=False)
            for status in status_options:
                options['status_options'].append(
                    {'id': status.id, 'state': status.state_id, 'name': status.name})
            return JsonResponse(options, status=200, safe=False)
        except Exception as err:
            return JsonResponse({}, status=200)


class StatusView(viewsets.ModelViewSet, BaseController):
    queryset = Status.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(detail=False, url_path='statusList/(?P<id>[^/]+)')
    def get_status_list(self, request, id):
        try:
            init_filter = Q(is_deleted=False, wf_id=id)
            wf_obj = Status.objects.filter(init_filter).order_by('id')
            serializer = StatusListSerializer(wf_obj, many=True)
            wf_data = serializer.data
            final_data = [dict(x) for x in wf_data]
            return JsonResponse(final_data, status=200, safe=False)
        except Exception as err:
            return JsonResponse([], status=200)

    def create(self, request):
        try:
            post_data = self.get_post_data(request)
            if post_data.get('id') not in self.noneList:
                status_obj = Status.objects.get(id=post_data.get('id'))
            else:
                status_obj = Status()
            status_obj.wf_id = post_data.get('wfId')
            status_obj.state_id = post_data.get('stateId')
            status_obj.name = post_data.get('status_temp')
            status_obj.stage = post_data.get('stage_temp')
            status_obj.save()
            return JsonResponse({'status': 'success', 'data': {'id': status_obj.id, 'state_name': status_obj.state.name}}, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error', 'data': {}}, status=200)


class RuleView(viewsets.ModelViewSet, BaseController):
    queryset = Rules.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(detail=False, url_path='rulesList/(?P<id>[^/]+)')
    def get_status_list(self, request, id):
        try:
            init_filter = Q(is_deleted=False, wf_id=id)
            wf_obj = Rules.objects.filter(init_filter).order_by('id')
            serializer = RulesListSerializer(wf_obj, many=True)
            wf_data = serializer.data
            final_data = [dict(x) for x in wf_data]
            return JsonResponse(final_data, status=200, safe=False)
        except Exception as err:
            return JsonResponse([], status=200)

    def create(self, request):
        try:
            post_data = self.get_post_data(request)
            if post_data.get('id') not in self.noneList:
                rules_obj = Rules.objects.get(id=post_data.get('id'))
            else:
                rules_obj = Rules()
            rules_obj.wf_id = post_data.get('wfId')
            rules_obj.is_stage_rule = post_data.get('is_stage_rule', False)
            rules_obj.if_state_id = post_data.get('if_state')
            rules_obj.if_status_id = post_data.get('if_status')
            rules_obj.if_stage = post_data.get('if_stage', '')
            rules_obj.then_state_id = post_data.get('then_state')
            rules_obj.then_status_id = post_data.get('then_status')
            rules_obj.name = post_data.get('name')
            rules_obj.save()
            return JsonResponse({'status': 'success', 'data': {'id': rules_obj.id}}, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error', 'data': {}}, status=200)


class NotifView(viewsets.ModelViewSet, BaseController):
    queryset = Notifications.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(detail=False, url_path='notifList/(?P<id>[^/]+)')
    def get_status_list(self, request, id):
        try:
            init_filter = Q(is_deleted=False, wf_id=id)
            wf_obj = Notifications.objects.filter(init_filter).order_by('id')
            serializer = NotificationsListSerializer(wf_obj, many=True)
            wf_data = serializer.data
            final_data = [dict(x) for x in wf_data]
            return JsonResponse(final_data, status=200, safe=False)
        except Exception as err:
            return JsonResponse([], status=200)

    def create(self, request):
        try:
            post_data = self.get_post_data(request)
            if post_data.get('id') not in self.noneList:
                notif_obj = Notifications.objects.get(id=post_data.get('id'))
            else:
                notif_obj = Notifications()
            notif_obj.wf_id = post_data.get('wfId')
            notif_obj.is_stage_notification = post_data.get(
                'is_stage_notification', False)
            notif_obj.state_id = post_data.get('state')
            notif_obj.status_id = post_data.get('status')
            notif_obj.stage = post_data.get('stage')
            notif_obj.subject = post_data.get('subject')
            notif_obj.body = self.get_text_editor_text(post_data.get('body'))
            notif_obj.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as err:
            return JsonResponse({'status': 'error'}, status=200)

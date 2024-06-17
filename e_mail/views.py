from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from e_mail.forms import MailingAddForm, ClientAddForm, SettingsAddForm, SettingsManagerForm
from e_mail.models import MailingMessage, Client, MailingSettings



class MailingListView(ListView):
    model = MailingMessage
    template_name = 'e_mail/e_mail_list.html'
    context_object_name = 'objects_list'


class MailingCreateView(CreateView):
    model = MailingMessage
    template_name = 'e_mail/e_mail_form.html'
    form_class = MailingAddForm
    success_url = reverse_lazy('e_mail:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        settings_form_set = inlineformset_factory(MailingMessage, MailingSettings, form=SettingsAddForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = settings_form_set(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = settings_form_set(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        mailing_template = form.save()
        self.object = form.save()
        self.object.owner = self.request.user
        mailing_template.owner = self.object.owner
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            mailing_template.save()
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = MailingMessage
    template_name = 'e_mail/e_mail_detail.html'
    context_object_name = 'objects_list'


class MailingUpdateView(UpdateView):
    model = MailingMessage
    template_name = 'e_mail/e_mail_update_form.html'
    form_class = MailingAddForm
    success_url = reverse_lazy('e_mail:home')
    perms = ('e_mail.view_mailingmessage', 'e_mail.view_mailingsettings', 'e_mail.toggle_active',
             'users.can_block', 'users.view_user')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        settings_form_set = inlineformset_factory(MailingMessage, MailingSettings, form=SettingsAddForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = settings_form_set(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = settings_form_set(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        mailing_template = form.save()
        self.object = form.save()
        self.object.owner = self.request.user
        mailing_template.owner = self.object.owner
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            mailing_template.save()
        return super().form_valid(form)

    def get_form_class(self):
        if self.request.user.is_staff or self.request.user.has_perms(perm_list=self.perms) \
                and not self.request.user.is_superuser:
            return SettingsManagerForm
        else:
            if self.request.user != self.get_object().owner:
                raise PermissionDenied
            else:
                return SettingsAddForm





class MailingDeleteView(DeleteView):
    model = MailingMessage
    template_name = 'e_mail/e_mail_confirm_delete.html'
    success_url = reverse_lazy('e_mail:home')


def settings_toggle_active(request, pk):
    mailing_item = get_object_or_404(MailingSettings, pk=pk)
    if mailing_item.is_active is True:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True
    mailing_item.save()
    return redirect(reverse('e_mail:settings_home'))




class ClientListView(ListView):
    model = Client
    template_name = 'clients/clients_list.html'
    context_object_name = 'objects_list'




class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/clients_detail.html'
    context_object_name = 'objects_list'




class ClientCreateView(CreateView):
    model = Client
    template_name = 'clients/clients_form.html'
    form_class = ClientAddForm
    success_url = reverse_lazy('e_mail:client_home')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)




class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'clients/clients_update_form.html'
    form_class = ClientAddForm
    success_url = reverse_lazy('e_mail:client_home')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)




class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/clients_confirm_delete.html'
    success_url = reverse_lazy('e_mail:client_home')


class SettingsListView(ListView):
    model = MailingSettings
    template_name = 'mail_settings/settings_list.html'
    context_object_name = 'objects_list'


class SettingsDetailView(DetailView):
    model = MailingSettings
    template_name = 'mail_settings/settings_detail.html'
    context_object_name = 'objects_list'


class SettingsCreateView(CreateView):
    model = MailingSettings
    template_name = 'mail_settings/settings_add_form.html'
    form_class = SettingsAddForm
    success_url = reverse_lazy('e_mail:settings_home')

    def form_valid(self, form):
        mailing_settings = form.save()
        user = self.request.user
        mailing_settings.owner = user
        mailing_settings.save()
        return super().form_valid(form)


class SettingsUpdateView(UpdateView):
    model = MailingSettings
    template_name = 'mail_settings/settings_update_form.html'
    form_class = SettingsAddForm
    success_url = reverse_lazy('e_mail:settings_home')

    def form_valid(self, form):
        mailing_settings = form.save()
        user = self.request.user
        mailing_settings.owner = user
        mailing_settings.save()
        return super().form_valid(form)


class SettingsDeleteView(DeleteView):
    model = MailingSettings
    template_name = 'mail_settings/settings_confirm_delete.html'
    success_url = reverse_lazy('e_mail:settings_home')

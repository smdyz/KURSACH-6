from django import forms

from e_mail.models import MailingMessage, Client, MailingSettings

WORDS_BLACKLIST = ('казино', 'криптовалюта', 'крипта', 'биржа', 'наркотики' 'бесплатно',
                   'обман', 'полиция', 'терракт')


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingAddForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = MailingMessage
        exclude = ('owner', )

    def clean_subject(self):
        cleaned_data = self.cleaned_data.get('subject')

        if cleaned_data in WORDS_BLACKLIST:
            raise forms.ValidationError('Тема письма содержит в себе запрещенные слова')

        return cleaned_data

    def clean_message(self):
        cleaned_data = self.cleaned_data.get('message')

        if cleaned_data in WORDS_BLACKLIST:
            raise forms.ValidationError('Письмо содержит в себе запрещенные слова')

        return cleaned_data


class ClientAddForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')

        if cleaned_data in WORDS_BLACKLIST:
            raise forms.ValidationError('У-пс, описание клиента содержит в себе слова из списка'
                                        'запрещённых слов')

        return cleaned_data


class SettingsAddForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        exclude = ('status', 'owner')

    def clean_mailing_name(self):
        cleaned_data = self.cleaned_data.get('mailing_name')

        if cleaned_data in WORDS_BLACKLIST:
            raise forms.ValidationError('Такую рассылку нельзя отправлять согласно уголовному кодексу Российской '
                                        'Федерации и политики нашей компании')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].widget.attrs['class'] = ''


class SettingsManagerForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        exclude = ('status', 'owner', 'client')

    def clean_mailing_name(self):
        cleaned_data = self.cleaned_data.get('mailing_name')

        if cleaned_data in WORDS_BLACKLIST:
            raise forms.ValidationError('У-пс, название рассылки в списке запрещённых товаров')

        return cleaned_data

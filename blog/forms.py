from django import forms

from blog.models import Blog

WORDS_BLACKLIST = ('казино', 'криптовалюта', 'крипта', 'биржа', 'наркотики' 'бесплатно',
                   'обман', 'полиция', 'терракт')


class RecordAddForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('is_published', 'views_count')

    def clean_title(self):
        cleaned_data = self.cleaned_data.get('title')
        if cleaned_data in WORDS_BLACKLIST:
            raise forms.ValidationError('У-пс, заголовок записи в списке запрещённых слов')

        return cleaned_data

    def clean_body(self):
        cleaned_data = self.cleaned_data.get('body')
        if cleaned_data in WORDS_BLACKLIST:
            raise forms.ValidationError('У-пс, в содержании записи есть слова из списка запрещённых слов')

        return cleaned_data

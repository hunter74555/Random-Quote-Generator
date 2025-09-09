from django import forms
from .models import Quote, Source


class QuoteForm(forms.ModelForm):
    source_name = forms.CharField(max_length=200, label="Название источника")
    source_type = forms.ChoiceField(choices=Source.SOURCE_TYPES, label="Тип источника")

    class Meta:
        model = Quote
        fields = ['text', 'weight']
        labels = {
            'text': 'Текст цитаты',
            'weight': 'Вес (чем больше, тем чаще показывается)'
        }

    def clean(self):
        cleaned_data = super().clean()
        source_name = cleaned_data.get('source_name')
        source_type = cleaned_data.get('source_type')

        if source_name and source_type:
            # Получаем или создаем источник
            source, created = Source.objects.get_or_create(
                name=source_name,
                type=source_type,
                defaults={'name': source_name, 'type': source_type}
            )

            # Проверяем ограничение на количество цитат у источника
            if not created and source.quote_set.count() >= 3:
                raise forms.ValidationError('У этого источника уже максимальное количество цитат (3)')

            cleaned_data['source'] = source

            # Проверяем уникальность цитаты для этого источника
            text = cleaned_data.get('text')
            if text and Quote.objects.filter(text=text, source=source).exists():
                raise forms.ValidationError('Такая цитата уже существует для этого источника')

        return cleaned_data

    def save(self, commit=True):
        quote = super().save(commit=False)
        quote.source = self.cleaned_data['source']
        if commit:
            quote.save()
        return quote
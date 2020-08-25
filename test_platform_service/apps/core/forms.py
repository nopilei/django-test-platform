from django import forms

from .models import Question, Test, Answer

import django_filters


class TestFilter(django_filters.FilterSet):
    DATE_SORT_CHOICES = [('ASC', 'По возрастанию'), ('DESC', 'По убыванию')]

    name = django_filters.CharFilter(lookup_expr='icontains')
    results__user = django_filters.BooleanFilter(widget=forms.CheckboxInput(),
                                                 label='Только не пройденные вами тесты',
                                                 method='exclude_passed')
    date_created_sorting = django_filters.ChoiceFilter(choices=DATE_SORT_CHOICES,
                                                       method='date_sort',
                                                       label='Сортировать по дате создания',
                                                       empty_label=None)

    def date_sort(self, queryset, name, value):
        if value == 'DESC':
            return queryset.order_by('-date_created')
        else:
            return queryset.order_by('date_created')

    def exclude_passed(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.exclude(**{name: self.request.user})
        elif not value:
            return queryset
        else:
            return queryset.none()


class BaseQuestionFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        if not all(self.cleaned_data):
            raise forms.ValidationError('Заполните все поля вопросов')


class BaseAnswerFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        if not all(self.cleaned_data):
            raise forms.ValidationError('Заполните все поля ответов')
        if list(map(lambda a: a['is_true'], self.cleaned_data)).count(True) != 1:
            raise forms.ValidationError('На вопрос должен быть 1 и только 1 правильный ответ')


class NumberOfQuestionsForm(forms.Form):
    MIN_NUMBER_OF_QUESTIONS = 5
    num_of_questions = forms.IntegerField(max_value=20,
                                          min_value=MIN_NUMBER_OF_QUESTIONS,
                                          initial=MIN_NUMBER_OF_QUESTIONS,
                                          label='Кол-во вопросов в тесте')


class TestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        fields = ['name', 'description']
        model = Test


class AnswerForm(forms.ModelForm):

    class Meta:
        fields = ['answer_text', 'is_true']
        model = Answer


class QuestionForm(forms.ModelForm):

    class Meta:
        fields = ['question_text']
        model = Question


QuestionFormSet = forms.inlineformset_factory(Test,
                                              Question,
                                              form=QuestionForm,
                                              formset=BaseQuestionFormset,
                                              can_delete=False,

                                              )
AnswerFormSet = forms.inlineformset_factory(Question,
                                            Answer,
                                            form=AnswerForm,
                                            extra=4,
                                            can_delete=False,
                                            formset=BaseAnswerFormset,
                                            )
from django.db import models
from django.db.models import F
from django.utils.timezone import now
from ..users.models import TestUser


class Test(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название теста')
    description = models.CharField(max_length=300, verbose_name='Описание')
    num_of_passes = models.IntegerField(default=0, verbose_name='Кол-во прохождений')
    author = models.ForeignKey(TestUser, on_delete=models.CASCADE,
                               related_name='tests', verbose_name='Автор',
                               null=True, blank=True)
    date_created = models.DateField(verbose_name='Дата создания', default=now)

    def __str__(self):
        return self.name

    def incr_num_of_passes(self):
        self.num_of_passes = F('num_of_passes') + 1
        self.save(update_fields=['num_of_passes'])

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    question_text = models.CharField(max_length=100, verbose_name='Текст вопроса')
    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             related_name='questions', verbose_name='Вопрос')

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    answer_text = models.CharField(max_length=200, verbose_name='Текст ответа')
    is_true = models.BooleanField(verbose_name='Правильный/Неправильный')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answers', verbose_name='Вопрос')

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class TestResult(models.Model):
    user = models.ForeignKey(TestUser, on_delete=models.CASCADE,
                             related_name='results', verbose_name='Пользователь' )
    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             related_name='results', verbose_name='Тест')
    result = models.FloatField(verbose_name='Результат (процентов)')

    def __str__(self):
        return f'{self.user}:{self.test}:{self.result}%'

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'


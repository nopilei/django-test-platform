from django.shortcuts import render, redirect
from django.contrib.messages import success, warning
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import NumberOfQuestionsForm, TestFilter
from .utils import get_all_forms, get_num_of_questions, save_test, get_test_result
from .models import Test


@login_required
def init_create_test(request):
    """Render form to select number of questions in test"""

    initial_form = NumberOfQuestionsForm()
    return render(request, 'core/init_create_test.html', {'form': initial_form})


@login_required
def complete_creation(request):
    """Render forms and formsets (TestForm, QuestionFormset, AnswerFormset)"""

    if request.method == 'GET':
        num_of_questions = get_num_of_questions(request.GET)
        test_form, questions_and_answers, question_formset = get_all_forms(num_of_questions)
    else:
        num_of_questions = request.POST['num_of_questions']
        test_form, questions_and_answers, question_formset, all_forms_are_valid = save_test(request)
        if all_forms_are_valid:
            success(request, 'Тест создан')
            return redirect('home')
        else:
            warning(request, 'Что-то не так. Перепроверьте информацию, введенную в формы')

    return render(request,
                  'core/creation_complete.html',
                  {
                      'test_form': test_form,
                      'questions_and_answers': questions_and_answers,
                      'question_formset': question_formset,
                      'num_of_questions': num_of_questions
                  }
                  )


def index(request):
    """Render main page with filtration"""
    tests = Test.objects.all()
    filter = TestFilter(request.GET, queryset=Test.objects.all(), request=request)
    return render(request, 'core/index.html', {'tests': tests, 'filter': filter})


def test_detail(request, pk):
    """Render test detail page"""
    test = get_object_or_404(Test, pk=pk)
    return render(request, 'core/test_detail.html', {'test': test})


@login_required
def pass_the_test(request, pk):
    """Given user's answers, get test's result """
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'GET':
        return render(request, 'core/test_passing.html', {'test': test})
    else:
        percentage = get_test_result(request, test)
        return render(request, 'core/test_result.html', {'percentage': percentage})

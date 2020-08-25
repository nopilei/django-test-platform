from django.http.request import QueryDict
from django.core.handlers.wsgi import WSGIRequest

from .forms import (NumberOfQuestionsForm, TestForm,
                    QuestionFormSet, AnswerFormSet,
                    QuestionForm)
from .models import TestResult, Test

from typing import Dict, Tuple

QAPairs = Dict[QuestionForm, AnswerFormSet]


def get_test_result(request: WSGIRequest, test: Test) -> float:
    """Count the number of right user's answers and return the percentage of right answers"""

    # set of primary keys of the right answers of all questions in test
    true_answers_pks = {str(q.answers.get(is_true=True).pk) for q in test.questions.all()}
    # number of right user's answers
    num_of_true_user_answers = len(set(request.POST.values()) & true_answers_pks)
    percentage = round(num_of_true_user_answers / len(true_answers_pks), 3) * 100
    # increment the number of test's passes
    test.incr_num_of_passes()
    # create TestResult object with the calculated percentage
    TestResult.objects.create(user=request.user, test=test, result=percentage)
    return percentage


def get_num_of_questions(get_params: QueryDict) -> int:
    """
    Fetch 'num_of_questions' parameter from request.GET

    If parameter is invalid or absent, get min value from NumberOfQuestionsForm
    """
    _min = NumberOfQuestionsForm.MIN_NUMBER_OF_QUESTIONS
    try:
        num_of_questions = int(get_params.get('num_of_questions', _min))
        num_of_questions = num_of_questions if num_of_questions >= _min else _min
    except ValueError:
        num_of_questions = _min
    return num_of_questions


def get_all_forms(num_of_questions: int, params: QueryDict = None) -> Tuple[TestForm, QAPairs, QuestionFormSet]:
    """
    Given number of questions, create all required forms and formsets

    This function can be used both with 'get' and 'post' methods.
    If argument 'params' if passed, it will create bounded forms with 'params'
    """
    test_form = TestForm(params)
    # dict to map question forms and answer formsets
    questions_and_answers = {}
    QuestionFormSet.extra = num_of_questions
    question_formset = QuestionFormSet(params)
    for ix, question in enumerate(question_formset):
        questions_and_answers[question] = AnswerFormSet(params, prefix=ix)
    return test_form, questions_and_answers, question_formset


def save_test(request: WSGIRequest) -> Tuple[TestForm, QAPairs, QuestionFormSet, bool]:
    """
    Save whole test via forms, with questions and answers attached

    If one of the forms or formsets (TestForm, QuestionFormset, AnswerFormset) is invalid, do not save the test
    """

    #Varible used later in view
    all_forms_are_valid = False
    test_form, questions_and_answers, question_formset = (
        get_all_forms(request.POST['num_of_questions'], request.POST)
    )
    if test_form.is_valid():
        test = test_form.save(commit=False)
        test.author = request.user
        question_formset = QuestionFormSet(request.POST, instance=test)
        if question_formset.is_valid():
            questions = question_formset.save(commit=False)
            #Accumulate answers in list to save later in loop
            #If one of the answers is invalid, discard all actions to save objects in database
            answers_to_save = []
            for ix, question in enumerate(questions):
                answer_formset = AnswerFormSet(request.POST, instance=question, prefix=ix)
                if answer_formset.is_valid():
                    answers_to_save.extend(answer_formset.save(commit=False))
                else:
                    break
            else:
                #If everything's fine, save all objects in database
                test_form.save()
                question_formset.save()
                for answer in answers_to_save:
                    answer.save()
                all_forms_are_valid = True
    return test_form, questions_and_answers, question_formset, all_forms_are_valid


from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from pybo.models import Question, Answer
from django.utils import timezone
from pybo.forms import AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.paginator import Paginator
from django.db.models import Q, Count

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    # 방법 1:
    # question.answer_set.create(content = request.POST.get("content"), create_date = timezone.now())
    
    # 방법 2:
    # answer = Answer(question = question, content = request.POST.get("content"), create_date = timezone.now())
    # answer.save()

    # return redirect('pybo:detail', question_id = question.id)

    # 방법 3:
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # return redirect('pybo:detail', question_id=question.id)
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail',question_id=question.id), answer.id))
    else:
        # return HttpResponseNotAllowed('Only POST is possible.')
        form = AnswerForm()
    
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    if so == 'recommend':
        answer_list = Question.answer_set.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        answer_list = Question.answer_set.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
        answer_list = Question.answer_set.objects.order_by('-create_date') 

    if kw:
        answer_list = answer_list.filter(
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)

    current_page = page_obj.number
    start_index = max(current_page - 5, 1)
    end_index = min(current_page + 5, paginator.num_pages)
    page_range = range(start_index, end_index + 1)



    context = {
        'question': question, 
        'form': form,
        'page_range': page_range, 
        'page': page, 
        'kw': kw,
        'so': so

    }
    return render(request, 'pybo/question_detail.html', context)
    

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            # return redirect('pybo:detail', question_id=answer.question.id)
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    # return redirect('pybo:detail', question_id=answer.question.id)
    return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))


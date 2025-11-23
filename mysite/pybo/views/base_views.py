from django.shortcuts import render, get_object_or_404
from pybo.models import Question
from django.core.paginator import Paginator
from django.db.models import Q, Count

def index(request):
    # request.GET: url의 쿼리스트링(? 뒤의 값)을 가져오기
    # http://127.0.0.1:8000/pybo/?page=1
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')
 
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
        question_list = Question.objects.order_by('-create_date') 
                                           
    # question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
        """
        select distinct q.*
        from pybo_question q
        left join pybo_answer a on a.question_id = q.id
        right join customuser c on c.id = a.author_id
        where q.subject ilike "%kw%"
            or q.content ilike "%kw%"
            or c.username ilike "%kw%"
        """

    # Question.object.all()로 확인할 결과는 p.63 참조
    # 쿼리셋으로 조회됨
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    current_page = page_obj.number
    start_index = max(current_page - 5, 1)
    end_index = min(current_page + 5, paginator.num_pages)
    page_range = range(start_index, end_index + 1)

    context = {
        'question_list': page_obj,
        'page_range': page_range, 
        'page': page, 
        'kw': kw,
        'so': so,
        'hostname': socket.gethostname()  # 추가

    }

    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
            'question': question,
            'hostname': socket.gethostname()
    }
    return render(request, 'pybo/question_detail.html', context)

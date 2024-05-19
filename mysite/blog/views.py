from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from .models import Post
from  django.views.decorators.http import require_POST


# def post_list(request):
#   post_list = Post.published.all()
#   paginator = Paginator(post_list, 3)
#   page_number = request.GET.get('page', 1)
#   # posts = paginator.page(page_number)
#   try:
#     posts = paginator.page(page_number)
#
#   except PageNotAnInteger:
#     posts = paginator.page(1)
#
#   except EmptyPage:
#     posts = paginator.page(paginator.num_pages)
#   return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
  # try:
  #   post = Post.published.get(id=id)
  # except Post.DoesNotExist:
  #   raise Http404('Пост не найден')
  post = get_object_or_404(Post,
                           status=Post.Status.PUBLISHED,
                           slug=post,
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)
  #список активных комментариев к этому посту
  comments = post.comments.filter(active=True)
  #форма для комментирования пользователями
  form = CommentForm()
  return render(request, 'blog/post/detail.html',
                {'post': post,
                 'comments': comments,
                 'form': form})

class PostListView(ListView):
  queryset = Post.published.all()
  context_object_name = 'posts'
  paginate_by = 3
  template_name = 'blog/post/list.html'


def post_share(request, post_id):
  # извлечь пост по индефекатору id
  post = get_object_or_404(Post,
                           id=post_id,
                           status=Post.Status.PUBLISHED)

  send = False

  if request.method == "POST":
    #форма была передана на обработку
    form = EmailPostForm(request.POST)
    if form.is_valid():
      #поля формы успешно прошли валидацию
      cd = form.cleaned_data
      post_url = request.build_absolute_uri(post.get_absolute_url())
      subject = f"{cd['name']} рекомендует вам прочитать {post.title}"
      massage = f"Прочитать {post.title} at {post_url} {cd['name']} комментарии: {cd['comments']}"
      send_mail(subject, massage, 'evamilya@bk.ru', [cd['to']])
      send = True
      #... отправить электронное письмо

  else:
    form = EmailPostForm()
  return render(request, 'blog/post/share.html', {'post': post,
                                                      'form': form,
                                                      'send': send})

@require_POST
def post_comment(request, post_id):
  post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
  comment = None

  #комментарий был отправлен
  form = CommentForm(data=request.POST)
  if form.is_valid():
    #создать объект класса Comment, не сохраняя его в базе данных
    comment = form.save(commit=False)
    #назначить пост комментария
    comment.post = post
    #сохранить комментарий в базе данных
    comment.save()
  return render(request, 'blog/post/comment.html', {'post': post,
                                                    'form': form,
                                                    'comment': comment})


from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse

def send_email_view(request):
    email = EmailMessage(
        subject='Внимание д/з',
        body='Это домашнее задание от 12 февраля 2024 года',
        from_email='Admin <evamilya@bk.ru>',
        to=['nadiamilyaeva@gmail.com', 'nadia.milyaeva@mail.ru'],
        )

    email.send()

    return HttpResponse('Письмо успешно отправлено!')




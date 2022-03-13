from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView
from .models import Post, Category
from datetime import datetime
from django.shortcuts import render
from .filters import PostFilter
from django.core.paginator import Paginator
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    model = Post
    template_name = 'Posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context[
            'value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostSearch(PostList):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'Search.html' # название HTML файла
    context_object_name = 'search'  # название объекта. в нём будет
    paginate_by = 10
    filter_class = PostFilter

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())  # вписываем наш фильтр в контекст

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        category_pk = request.POST.get('categories')
        text = request.POST.get('text')
        header = request.POST.get('header')
        category = Category.objects.get(pk=category_pk)
        subscribers = category.subscribers.all()
        host = request.META.get('HTTP_HOST')

        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            print('Статья:', news)

        for subscriber in subscribers:
            print('Адреса рассылки:', subscriber.email)

            html_content = render_to_string(
             'mail_sender.html', {'user': subscriber, 'text': text[:50], 'post': news, 'host': host})

            msg = EmailMultiAlternatives(
                 subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
                 body=f'{text[:50]}',
                 from_email='newspost1@yandex.ru',
                 to=[subscriber.email],
                )

            msg.attach_alternative(html_content, "text/html")
            print(html_content)
            msg.send()

        return redirect('/news/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        qwe = Category.objects.filter(pk=Post.objects.get(pk=id).categories.id).values("subscribers__username")
        context['is_not_subscribe'] = not qwe.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = qwe.filter(subscribers__username=self.request.user).exists()
        return context


@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk')
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')


# функция отписки от группы
@login_required
def del_subscribe(request, **kwargs):
    pk = request.GET.get('pk')
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/')


class PostCreateView(CreateView, PermissionRequiredMixin):
    template_name = 'post_create.html'
    form_class = PostForm
    success_url = '/news/'
    #permission_required = ('news.add_post')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)  # общаемся к содержимому контекста нашего представления
    #     id = self.kwargs.get('pk')  # получаем ИД поста (выдергиваем из нашего объекта из модели Пост)
    #     # формируем запрос, на выходе получим список имен пользователей subscribers__username, которые находятся
    #     # в подписчиках данной группы, либо не находятся
    #     qwe = Category.objects.filter(pk=Post.objects.get(pk=id).categories.id).values("subscribers__username")
    #     # Добавляем новую контекстную переменную на нашу страницу, выдает либо правду, либо ложь, в зависимости от
    #     # нахождения нашего пользователя в группе подписчиков subscribers
    #     context['is_not_subscribe'] = not qwe.filter(subscribers__username=self.request.user).exists()
    #     context['is_subscribe'] = qwe.filter(subscribers__username=self.request.user).exists()
    #     return context


class PostUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post')

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context




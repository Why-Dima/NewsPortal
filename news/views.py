from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import Post
from datetime import datetime
from django.shortcuts import render
from .filters import PostFilter
from django.core.paginator import Paginator
from .forms import PostForm


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
    template_name = 'Search.html'  # название шаблона будет product.html
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


class PostCreateView(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

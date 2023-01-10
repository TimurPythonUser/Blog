from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView


from .forms import *
from .models import *
from .utils import DataMixin


class PostHome(DataMixin, ListView):
    paginate_by = 2
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-id')
        return queryset


def show_detail_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comms = Comments.objects.filter(comment=post_id).order_by('-id')
    likes = post.total_likes()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    if request.method == 'POST':
        form2 = AddComment(request.POST, prefix='form2')
        if form2.is_valid():
            form2 = form2.save(commit=False)
            form2.author = request.user
            form2.comment = post
            form2.save()
            return redirect(show_detail_post, post_id)
    else:
        form2 = AddComment()
    return render(request, 'myblog/detail.html', {'post': post, 'comms': comms,
                                                  'form2': form2, 'likes': likes, 'liked': liked})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('detail', args=[str(pk)]))


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'myblog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'myblog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'myblog/addpost.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить публикацию')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ShowPost(DataMixin, ListView):
    paginate_by = 1
    model = Post
    template_name = 'myblog/showauthorpost.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'posts'
    extra_context = {'title': 'Мои публикации'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['posts'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


def logout_user(request):
    logout(request)
    return redirect('home')


class SearchResult(DataMixin, ListView):
    model = Post
    template_name = 'myblog/searchres.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = Post.objects.filter(category__contains=q)
        return queryset




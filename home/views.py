#home/view.py
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from home.forms import PostForm, CommentForm
from home.models import Post, Comment
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        posts = Post.objects.all().order_by('-created')
        comments = Comment.objects.all().order_by('-created')
        nb_comments = 3

        args = {
                'posts':posts,
                'comments':comments,
                'nb_comments': nb_comments
                }
        return render(request, self.template_name, args)


@method_decorator(login_required, name='dispatch')
class NewPostView(TemplateView):
    template_name='home/new_post.html'

    def get(self, request):
        form = PostForm()
        args={'form':form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user=request.user
            post.save()

            text = form.cleaned_data['text']
            form = PostForm()
            return redirect('home')

        args = {'form':form, 'text':text}
        return render(request, self.template_name, args)

@method_decorator(login_required, name='dispatch')
class EditPostView(TemplateView):
    template_name='home/edit_post.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        args={'form':form}
        return render(request, self.template_name, args)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user=request.user
            post.save()

            text = form.cleaned_data['text']
            form = PostForm(instance=post)
            return redirect('home')

        args = {'form':form, 'text':text}
        return render(request, self.template_name, args)

class PostView(TemplateView):
    template_name = 'home/post.html'

    def get(self, request, pk):
        form = CommentForm()
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.all().order_by('-created')

        args = {
                'form': form,
                'post': post,
                'comments':comments
                }
        return render(request, self.template_name, args)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            comment_text = form.cleaned_data['text']
            form = CommentForm()
            return redirect('post', pk=post.pk)
        args = {'form':form, 'comment_text':comment_text}
        return render(request, self.template_name, args)

@method_decorator(login_required, name='dispatch')
class DeletePost(TemplateView):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('home')

@method_decorator(login_required, name='dispatch')
class CommentRemove(TemplateView):

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('post', pk=comment.post.pk)

@method_decorator(login_required, name='dispatch')
class CommentEdit(TemplateView):
    template_name = 'home/edit_comment.html'
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            comment_text = form.cleaned_data['text']
            form = CommentForm()
            return redirect('post', pk=post.pk)
        args = {'form':form, 'comment_text':comment_text}
        return render(request, self.template_name, args)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CustomerUserCreationForm, UserEditForm, ProfileEditForm, PostCreateEditForm, CommentForm
from .models import Post, Comment
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.db.models import Q


class RegisterView(CreateView):
    """
    A class-based view for user registration using Django's CreateView.
    Attributes:
        form_class: Specifies the form to use for creating the user.
        template_name: The path to the HTML template to use for the registration page.
        success_url: Redirect URL which is used on successful creation, here to the login page.
    """
    form_class = CustomerUserCreationForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')


def search(request):
    """
        first we get searched which is either a query or none
        we check if searched , we get it using request.GET['searched']
        then using Q to be able to have multiple search queries at once either by the title, content or the tag naame
        and we filter that , then we return it into context
    """
    searched = request.GET.get('searched', '')
    if 'searched' in request.GET:
        searched = request.GET['searched']
        multiple_q = Q(
            Q(title__icontains=searched) | Q(tags__name__icontains=searched) | Q(content__icontains=searched))
        posts = Post.objects.filter(multiple_q)
    else:
        posts = Post.objects.all()
    return render(request, 'blog/search.html', {'posts': posts, 'searched': searched})


def home(request):
    return render(request, "blog/home.html")


@login_required
def profile_update(request, pk):
    """
      A view function for updating a user's profile.
      Args:
          request: The HTTP request object.
          pk (int): The primary key of the user whose profile is to be updated.
      Workflow:
      - First, checks if the logged-in user is the same as the user who is intended to be edited.
      - If the user is authenticated and the request method is POST, handle form submission.
      - If both forms are valid, save them and redirect to the user's profile page.
      - If not POST, instantiate forms with the existing user and profile data.
      Raises:
          Http404: If the logged-in user is not the same as the user whose profile is intended to be edited.
      """
    if request.user.pk != int(pk):
        raise Http404('you are not allowed to edit another profile')
    user = User.objects.get(id=pk)
    profile = user.profile

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', pk=request.user.pk)

    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'blog/edit_profile.html', context=context)


class PostListView(ListView):
    """
        Displays a list of all the posts with a custom object name
         so its easy to loop on all posts instead of object name
         no authentication and accessible to everyone
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    """
        Displays single post with a custom object name
         no authentication and accessible to everyone,
         adding get_context_data so i can dynamically load the CommentForm in the Detail post
         to make it easier to add comments
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context


class PostCreateView(CreateView):
    """
        create a Post using the PostCreateEditForm , with a template name
        and using reverse lazy to the main page upon Creating
        overriding the form_valid method to auto assign author to be the logged in user
    """
    model = Post
    form_class = PostCreateEditForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostByTagListView(ListView):
    """
        a view to return posts by specific tags
        using Post model and posts as object_name
        i override the get_quertyset so i can filter the query by only the posts with the tags in the tag_slug
        and overriding the context_data to pass in extra information which is the tag_name
        so i can use it in the template saying Posts tagged with {{tag_name}}
    """
    model = Post
    template_name = 'blog/tagged_posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__name__in=[self.kwargs['tag_slug']])

    def get_context_data(self, **kwargs):
        context = super(PostByTagListView, self).get_context_data(**kwargs)
        context['tag_name'] = self.kwargs['tag_slug']
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
        Update a Post using the PostCreateEditForm , with a template name
        and using reverse lazy to the main page upon updating
        only logged in users are allowed to update posts using LogginRequiredMixin,
        and every user can only update his own posts using UserPassesTestMixin by using test_func
        getting the post using self.get_objects then return True of False based if the post.author is the same as
        the logged in user
    """
    model = Post
    form_class = PostCreateEditForm
    template_name = "blog/post_update.html"
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
        Delete a Post , with a template name
        and using reverse lazy to the main page upon Deleting
        only logged in users are allowed to delete posts using LogginRequiredMixin,
        and every user can only delete his own posts using UserPassesTestMixin by using test_func
        getting the post using self.get_objects then return True of False based if the post.author is the same as
        the logged in user
    """
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
        Class to create Comments using CreateView , taking the Comment Model
        using CommentForm to handle the Comment creation ,
        overriding the form_valid to auto assign the post and the author to the comment

        Using form.instance to get the comment then .post to assign  its related post
        then getting Post.objects.get(id=self.kwargs['pk'] to get the post id from the URL

        using form.instance to get the comment then .author to assign its author
        then using self.request.user to assign it to the logged in user

        overriding the get_success_url using to be able to redirect to the related post
        using kwargs={'pk' , self.kwargs['pk'} to again assign the pk to the post from URL
    """
    model = Comment
    form_class = CommentForm
    template_name = "blog/comments_create.html"

    def form_valid(self, form):
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
        Class to update the comment, using the same form_class and taking the comment model
        no need to assign the post or the author again as its already assigned because we r updating a comment
        over riding the success_url using kwargs={'pk':self.object.post.pk} self.object refering to the comment
        and .post.pk to get the related post pk as its not in the URL now

        using loginrequiredmixin to allow only logged in user to update comment and userpassestest mixing
        with test_func that returns true only if the comment author is the same as logged in user
    """
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_update.html"

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
        Delete a comment with over riding the success url and using authentication with login required
        and user passes test to only allow same user to delete his own comments
    """
    model = Comment
    template_name = "blog/comment_delete.html"

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

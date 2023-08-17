from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from .models import Post, Comment, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm, AddPostForm, LoginForm, UserRegisterationForm, UserEditForm, ProfileEditForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector,rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            return render(request, 'blog/search.html', {'form':form, 'query':query, 'results':results})
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/list.html', {'posts':posts, 'tag':tag,'form':form, 'query':query, 'results':results})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,slug=post, publish__year=year, publish__month=month,
                                publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    
    return render(request, 'blog/detail.html', {'post':post,'comments': comments,'form': form,'similar_posts': similar_posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'snchorsiya008@gmail.com',
                      [cd['to']])
            sent = True
            print('Email Sned:', sent)
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post':post, 'form':form, 'sent':sent })


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
 # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
 # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
 # Assign the post to the comment
        comment.post = post
 # Save the comment to the database
        comment.save()
    return render(request, 'blog/comment.html',{'post': post,'form': form, 'comment': comment})



def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector,rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')

    return render(request, 'blog/search.html', {'form':form, 'query':query, 'results':results})

@login_required
def add_post(request):
    form = AddPostForm()
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:post_list')
        
    return render(request, 'blog/addpost.html', {'form':form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user is not None:
                  if user.is_active: 
                    login(request,user)
                    return redirect('blog:post_list')
            else:
                    return HttpResponse("Disable Account")
        else:
            return HttpResponse("Invalid Login")
    else:
        form = LoginForm()
    
    return render(request, 'blog/login.html', {'form':form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("blog:login")


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            existing_profile = Profile.objects.filter(user=new_user).first()
            if existing_profile:
                print('Profile already exist:')
            else:
                Profile.objects.create(user=new_user)
            return render(request,'blog/register_done.html', {'new_user':new_user})
        
    else:
        user_form = UserRegisterationForm()
    return render(request, 'blog/register.html', {'user_form':user_form})


@login_required
def edit(request):
  if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
             user_form.save()
             profile_form.save()
             messages.success(request, 'Profile updated successfully')
             return redirect('blog:post_list')
        else:
            messages.error(request, 'Error updating your profile')
  else:
      user_form = UserEditForm(instance=request.user)
      profile_form = ProfileEditForm(instance=request.user.profile)
  return render(request,'blog/edit.html',{'user_form': user_form,'profile_form': profile_form})


    


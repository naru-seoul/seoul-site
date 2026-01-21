from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Post, Comment
from .forms import PostForm, CommentForm


# 홈
def home(request):
    latest_posts = Post.objects.all().order_by("-id")[:5]
    return render(request, "home.html", {"latest_posts": latest_posts})


# 게시글 목록
def post_list(request):
    posts = Post.objects.all().order_by("-id")
    return render(request, "boards/post_list.html", {"posts": posts})


# 게시글 상세
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 조회수 증가
    post.views += 1
    post.save()

    comment_form = CommentForm()
    return render(
        request,
        "boards/post_detail.html",
        {
            "post": post,
            "comment_form": comment_form,
        },
    )


# 게시글 작성
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("boards:detail", pk=post.pk)
    else:
        form = PostForm()

    return render(request, "boards/post_form.html", {"form": form})


# 댓글 작성
@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect("boards:detail", pk=pk)


# 좋아요 토글
@login_required
def post_like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("boards:detail", pk=pk)


# 게시글 수정
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("boards:detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "boards/post_form.html", {"form": form})


# 게시글 삭제
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == "POST":
        post.delete()
        return redirect("boards:list")

    return render(request, "boards/post_confirm_delete.html", {"post": post})


# 댓글 삭제
@login_required
def comment_delete(request, pk, comment_pk):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_pk, post=post)

    if comment.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == "POST":
        comment.delete()

    return redirect("boards:detail", pk=pk)


# 댓글 수정 ✅
@login_required
def comment_update(request, pk, comment_pk):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_pk, post=post)

    if comment.author != request.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("boards:detail", pk=pk)
    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        "boards/comment_form.html",
        {
            "form": form,
            "post": post,
            "comment": comment,
        },
    )

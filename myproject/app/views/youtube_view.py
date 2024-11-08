from django.shortcuts import redirect

def redirect_to_google_activity(request):
    return redirect("https://myactivity.google.com/page?hl=ko&utm_medium=web&utm_source=youtube&page=youtube_comments")

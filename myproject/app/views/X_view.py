from django.shortcuts import redirect


def redirect_to_twitter_home(request):
    return redirect("https://twitter.com/home")

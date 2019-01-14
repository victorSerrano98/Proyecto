from django.shortcuts import render, render_to_response

def homePage(request):
    return render(request, 'home_page.html')
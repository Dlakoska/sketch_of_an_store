from django.shortcuts import render


def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        print(f'name: {name}, email: {email}')
    return render(request, 'home.html')


def contacts(request):
    return render(request, 'contacts.html')
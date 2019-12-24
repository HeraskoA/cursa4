import os
import random
import string

import os
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.conf import settings
from django.views.generic.base import View

from git import Repo as GitRepo

from .forms import AddRepoForm, NeuralForm
from .models import Repo
from .neyronka import CustomLinearRegression

neyronka = CustomLinearRegression()
neyronka.train()


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class MainView(CreateView, ListView):
    template_name = 'main.html'
    success_url = reverse_lazy('main')
    form_class = AddRepoForm

    def get_queryset(self):
        return Repo.objects.filter(user=self.request.user, is_test=False)

    def form_valid(self, form):
        repo = form.save(commit=False)
        repo.user = self.request.user

        repo_dir = ''.join(random.choice(string.ascii_letters + string.digits)
                           for _ in range(10))
        repo.relative_dir = repo_dir

        repo.save()

        GitRepo.clone_from(repo.deep_link, os.path.join(settings.REPOS_DIR, repo_dir))
        return redirect(self.success_url)


class RepoView(DetailView):
    model = Repo
    template_name = 'repo.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = f'./docs/repos/{self.get_object().relative_dir}/'
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                if '.html' in file:
                    files.append(os.path.join(r, file).replace(f"./docs/repos/", ""))
        context["files"] = files
        return context

    def get(self, request, *args, **kwargs):
        if 'remove' in request.GET.keys():
            self.get_object().delete()
            return redirect(self.success_url)
        elif 'generate' in request.GET.keys():
            os.system(f"pycco repos/{self.get_object().relative_dir}/**/*.py -p")
            #pass
        elif 'update' in request.GET.keys():
            repo = GitRepo(os.path.join(settings.REPOS_DIR, self.get_object().relative_dir))
            o = repo.remotes.origin
            o.pull()

        return super().get(request, *args, **kwargs)


def neural(request):
    if request.method == 'POST':
        form = NeuralForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data.get('year')
            repo_count = neyronka.predict(year)
            form = NeuralForm(initial={"year": year, "repo_count": repo_count})
            return render(request, 'neural.html', {'form': form})
    else:
        form = NeuralForm()
    return render(request, 'neural.html', {'form': form})


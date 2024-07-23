from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Skill, Title, UserStats, Language, Job, Quest, Reflection
from .forms import (
    TitleFormSet,
    JobFormSet,
    SkillFormSet,
    ReflectionForm,
    setup_level_formset,
    StatsForm,
    LanguageFormSet,
    setup_language_comprehension_formset,
    SignUpForm,
    QuestForm,
    DescriptionForm,
    QuestCompletionForm,
)
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.urls import reverse


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user_stats = UserStats.objects.create(user=user)
            user_stats.save()
            login(request, user)
            return redirect(stats_page)

    else:
        form = SignUpForm()

    return render(request, 'status_info/signup.html', {'form': form})


def logout_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'status_info/logout_page.html')


@login_required(login_url="/login")
def stats_page(request):
    user = request.user
    username = user.username
    stats = UserStats.objects.get(user=user)
    titles = Title.objects.filter(user=user)
    current_job_list = Job.objects.filter(user=user, current=True)
    current_job = 'None'
    if current_job_list.exists():
        current_job = current_job_list[0]
    jobs = Job.objects.filter(user=user, current=False)
    passive_skills = Skill.objects.filter(user=user, active=False)
    active_skills = Skill.objects.filter(user=user, active=True)
    languages = Language.objects.filter(user=user).order_by('-comprehension')

    context = {
        'user': user, 'username': username, 'titles': titles,
        'current_job': current_job, 'jobs': jobs, 'stats': stats,
        'passive_skills': passive_skills, 'active_skills': active_skills,
        'languages': languages,
    }

    return render(request, 'status_info/stats_page.html', context)


def update_object_description(object, form):
    if object.description == form.cleaned_data.get("description"): return
    object.description = form.cleaned_data.get("description")
    object.save()


@login_required(login_url="/login")
def skill_detail(request, skill_name):
    user = request.user
    skill = get_object_or_404(Skill, user=user, name=skill_name)
    form = DescriptionForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            update_object_description(skill, form)
            return HttpResponseRedirect(request.path_info)

    return render(request, 'status_info/detail_page.html', {'user': user, 'object': skill, 'form': form})


@login_required(login_url="/login")
def job_detail(request, job_name):
    user = request.user
    job = get_object_or_404(Job, user=user, name=job_name)
    form = DescriptionForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            update_object_description(job, form)
            return HttpResponseRedirect(request.path_info)

    return render(request, 'status_info/detail_page.html', {'user': user, 'object': job, 'form': form})


@login_required(login_url="/login")
def title_detail(request, title_name):
    user = request.user
    title = get_object_or_404(Title, user=user, name=title_name)
    form = DescriptionForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            update_object_description(title, form)
            return HttpResponseRedirect(request.path_info)

    return render(request, 'status_info/detail_page.html', {'user': user, 'object': title, 'form': form})


@login_required(login_url="/login")
def quests_page(request):
    user = request.user
    quests = Quest.objects.filter(user=user, completed=False).order_by('-date')
    old_quests = Quest.objects.filter(user=user, completed=True).order_by('-date')
    completion_form = QuestCompletionForm(user=request.user)

    context = {
        'user': user,
        'quests': quests,
        'old_quests': old_quests,
        'form': completion_form
    }

    return render(request, 'status_info/quests_page.html', context)


@login_required(login_url="/login")
def create_quest(request):
    user = request.user
    quest_form = QuestForm(request.POST or None, user=request.user)

    if request.method == 'POST':
        if quest_form.is_valid():
            instance = quest_form.save(commit=False)
            instance.user = user
            instance.completed = False
            instance.save()
            return redirect('quests_page')

    return render(request, 'status_info/quest_creation_page.html', {'form': quest_form})


@login_required(login_url="/login")
def quest_completion_post(request):
    if request.method == 'POST':
        form = QuestCompletionForm(request.POST, user=request.user)
        if form.is_valid():
            quest = Quest.objects.get(user=request.user, name=form.cleaned_data["quest_name"])
            quest.completed = form.cleaned_data["complete"]
            quest.save()
            return JsonResponse({'success': True})
        return JsonResponse({'errors': form.non_field_errors(), 'success': False})


@login_required(login_url="/login")
def reflection_page(request):
    user = request.user
    reflections = Reflection.objects.filter(user=user).order_by('-date')

    return render(request, 'status_info/reflection_page.html', {'user': user, 'reflections': reflections})


@login_required(login_url="/login")
def create_reflection(request):
    user = request.user
    reflection_form = ReflectionForm(request.POST or None, prefix="reflection")
    title_formset = TitleFormSet(request.POST or None, prefix="titles")
    job_formset = JobFormSet(request.POST or None, prefix="jobs")
    skill_formset = SkillFormSet(request.POST or None, prefix="skills")
    level_formset = setup_level_formset(request.POST or None, user, prefix="levels")
    stats_form = StatsForm(request.POST or None, prefix="stats_incr")
    language_formset = LanguageFormSet(request.POST or None, prefix="langs")
    lang_compr_formset = setup_language_comprehension_formset(request.POST or None, user, prefix="langs_compr")

    context = {
        'reflection_form': reflection_form,
        'title_formset': title_formset,
        'job_formset': job_formset,
        'skill_formset': skill_formset,
        'level_formset': level_formset,
        'stats_form': stats_form,
        'language_formset': language_formset,
        'lang_compr_formset': lang_compr_formset,
    }

    return render(request, 'status_info/reflection_creation_page.html', context)


def process_titles_input(title_formset, user):
    if title_formset.total_form_count() == 0: return ''
    response_data = "You acquired the "
    for num, title in enumerate(title_formset):
        response_data += '[' + title.cleaned_data["name"] + ']'
        if num + 1 != title_formset.total_form_count():
            response_data += ', '
        instance = title.save(commit=False)
        instance.user = user
        instance.save()
    response_data += ' Title'
    if title_formset.total_form_count() > 1: response_data += 's'
    response_data += '!\n'
    return response_data


def process_jobs_input(job_formset, user):
    if job_formset.total_form_count() == 0: return ''
    response_data = "You acquired the "
    for num, job in enumerate(job_formset):
        response_data += '[' + job.cleaned_data["name"] + ']'
        instance = job.save(commit=False)
        instance.current = True
        if num + 1 != job_formset.total_form_count():
            response_data += ', '
            instance.current = False
        instance.user = user
        instance.save()
    response_data += ' Job'
    if job_formset.total_form_count() > 1: response_data += 's'
    response_data += '!\n'
    return response_data


def process_skills_input(skill_formset, user):
    if skill_formset.total_form_count() == 0: return ''
    response_data = "You acquired the "
    for num, skill in enumerate(skill_formset):
        response_data += '[' + skill.cleaned_data["name"] + ': Level 1]'
        instance = skill.save(commit=False)
        instance.user = user
        instance.save()
        if num + 1 != skill_formset.total_form_count():
            response_data += ', '
    response_data += ' Skill'
    if skill_formset.total_form_count() > 1: response_data += 's'
    response_data += '!\n'
    return response_data


def process_levels_input(level_formset, user):
    if level_formset.total_form_count() == 0: return ''
    response_data = "The Levels of the "
    for num, level in enumerate(level_formset):
        skill_name = level.cleaned_data["skill_name"]
        skill = Skill.objects.get(user=user, name=skill_name)
        response_data += '[' + skill_name + ': ' + ' Level ' + str(skill.level) + ']'
        skill.level = skill.level + level.cleaned_data["increase"]
        skill.save()
        if num + 1 != level_formset.total_form_count():
            response_data += ', '
    response_data += ' Skill'
    if level_formset.total_form_count() > 1: response_data += 's'
    response_data += ' have increased!\n'
    return response_data


def process_languages_input(language_formset, user):
    if language_formset.total_form_count() == 0: return ''
    response_data = "You comprehended the "
    for num, language in enumerate(language_formset):
        response_data += '[' + language.cleaned_data["name"] +\
                         ': ' + str(language.cleaned_data["comprehension"]) + '%]'
        instance = language.save(commit=False)
        instance.user = user
        instance.save()
        if num + 1 != language_formset.total_form_count():
            response_data += ', '
    response_data += ' Language'
    if language_formset.total_form_count() > 1: response_data += 's'
    response_data += '!\n'
    return response_data


def process_lang_incr_input(lang_compr_formset, user):
    if lang_compr_formset.total_form_count() == 0: return ''
    response_data = ''
    for num, lang_compr in enumerate(lang_compr_formset):
        response_data += "Your comprehension of "
        lang_name = lang_compr.cleaned_data["lang_name"]
        increase = lang_compr.cleaned_data["increase"]
        lang = Language.objects.get(user=user, name=lang_name)
        response_data += '[' + lang_name + ': ' + str(lang.comprehension) + '%]'
        lang.comprehension = lang.comprehension + increase
        lang.save()
        response_data += ' increased by ' + str(increase) + '% !'
        if num + 1 != lang_compr_formset.total_form_count():
            response_data += '\n'
    return response_data


def process_stats_input(stats_form, user):
    if not stats_form.is_valid(): return ''
    response_data = ''
    user_stats = UserStats.objects.get(user=user)
    frontend_incr = stats_form.cleaned_data['frontend_incr']
    backend_incr = stats_form.cleaned_data['backend_incr']
    data_science_incr = stats_form.cleaned_data['data_science_incr']
    data_base_incr = stats_form.cleaned_data['data_base_incr']
    if frontend_incr != 0:
        frontend_current = user_stats.frontend_stat
        response_data += f'[Frontend: {frontend_current} -> {frontend_current + frontend_incr}]\n'
        user_stats.frontend_stat = frontend_current + frontend_incr
    if backend_incr != 0:
        backend_current = user_stats.backend_stat
        response_data += f'[Backend: {backend_current} -> {backend_current + backend_incr}]\n'
        user_stats.backend_stat = backend_current + backend_incr
    if data_science_incr != 0:
        data_science_current = user_stats.data_science_stat
        response_data += f'[Data Science: {data_science_current} -> {data_science_current + data_science_incr}]\n'
        user_stats.data_science_stat = data_science_current + data_science_incr
    if data_base_incr != 0:
        data_base_current = user_stats.data_base_stat
        response_data += f'[Data Bases: {data_base_current} -> {data_base_current + data_base_incr}]\n'
        user_stats.data_base_stat = data_base_current + data_base_incr

    user_stats.save()

    return response_data


@login_required(login_url="/login")
def reflection_post(request):
    if request.method == 'POST':
        user = request.user
        reflection_form = ReflectionForm(request.POST or None, prefix="reflection")
        stats_form = StatsForm(request.POST or None, prefix="stats_incr")
        title_formset = TitleFormSet(request.POST or None, user=user, prefix="titles")
        job_formset = JobFormSet(request.POST or None, user=user, prefix="jobs")
        skill_formset = SkillFormSet(request.POST or None, user=user, prefix="skills")
        level_formset = setup_level_formset(request.POST or None, user, prefix="levels")
        language_formset = LanguageFormSet(request.POST or None, user=user, prefix="langs")
        lang_compr_formset = setup_language_comprehension_formset(request.POST or None, user, prefix="langs_compr")
        response_data = {"errors": {}, "success": False}

        formsets_and_prefixs = {"titles": title_formset, "jobs": job_formset, "skills": skill_formset,
                                "levels": level_formset, "langs": language_formset, "langs_compr": lang_compr_formset}

        for prefix, formset in formsets_and_prefixs.items():
            if formset.total_form_count() > 0:
                if formset.is_valid(): continue
                response_data["errors"].update({prefix: formset.non_form_errors()})

        if response_data["errors"] != {}:
            return JsonResponse(response_data)

        result_gains = ''
        result_gains += process_stats_input(stats_form, request.user)
        result_gains += process_titles_input(title_formset, user)
        result_gains += process_jobs_input(job_formset, user)
        result_gains += process_skills_input(skill_formset, user)
        result_gains += process_levels_input(level_formset, user)
        result_gains += process_languages_input(language_formset, user)
        result_gains += process_lang_incr_input(lang_compr_formset, user)

        if reflection_form.is_valid():
            instance = reflection_form.save(commit=False)
            instance.gains = result_gains
            instance.user = user
            instance.save()
            response_data["success"] = True

        return JsonResponse(response_data)

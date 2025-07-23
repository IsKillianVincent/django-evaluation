from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserUpdateForm
from accounts.models import Skill, Language, UserSkill, UserLanguage
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from accounts.forms import UserExperienceForm

@login_required
def custom_password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Votre mot de passe a été modifié avec succès.")
            return redirect('profil')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/password_change.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile_view(request):
    user = request.user
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user)
    skills = Skill.objects.all()
    languages = Language.objects.all()

    if request.method == "POST":
        if form.is_valid():
            form.save()

        selected_skill_ids = request.POST.getlist("skills")
        UserSkill.objects.filter(user=user).exclude(skill_id__in=selected_skill_ids).delete()
        for skill_id in selected_skill_ids:
            skill = Skill.objects.filter(id=skill_id).first()
            if skill and not UserSkill.objects.filter(user=user, skill=skill).exists():
                UserSkill.objects.create(user=user, skill=skill)

        selected_languages = request.POST.getlist("languages")

        existing_language_ids = [int(lang_id) for lang_id in selected_languages]
        UserLanguage.objects.filter(user=user).exclude(language_id__in=selected_languages).delete()

        for lang_id in selected_languages:
            level = request.POST.get(f"level_{lang_id}")
            if not level:
                continue  # Langue cochée mais pas de niveau, on ignore (ou tu peux afficher un message)
            
            lang = Language.objects.filter(id=lang_id).first()
            if not lang:
                continue

            UserLanguage.objects.update_or_create(
                user=user,
                language=lang,
                defaults={"level": level}
            )

        return redirect('profile')

    LANGUAGE_LEVELS = ["Débutant", "Intermédiaire", "Avancé", "Bilingue"]

    user_languages = user.user_languages.all()
    language_levels_dict = {ul.language.id: ul.level for ul in user_languages}

    user_language_map = {ul.language_id: ul.level for ul in user.user_languages.all()}

    for language in languages:
        language.current_level = user_language_map.get(language.id)

    return render(request, 'accounts/edit_profile.html', {
        "form": form,
        "skills": skills,
        "languages": languages,
        "user_skill_ids": user.user_skills.values_list("skill_id", flat=True),
        "user_languages": user_languages,
        "language_levels": UserLanguage.LEVEL_CHOICES,
        "language_levels_dict": language_levels_dict,
    })

@login_required
def add_experience_view(request):
    if request.method == "POST":
        form = UserExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            messages.success(request, "Expérience ajoutée.")
            return redirect('profile')
    else:
        form = UserExperienceForm()
    
    return render(request, 'experience/add_experience.html', {'form': form})

@login_required
def delete_experience_view(request, experience_id):
    exp = UserExperience.objects.filter(id=experience_id, user=request.user).first()
    if exp:
        exp.delete()
        messages.success(request, "Expérience supprimée.")
    return redirect('profile')
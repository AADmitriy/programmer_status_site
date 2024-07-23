from django import forms
from .models import Skill, Language, Title, Job, Reflection, Quest
from django.forms.models import modelformset_factory, formset_factory
from django.utils.translation import gettext_lazy as _
from django.forms import BaseFormSet
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as djangoUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = djangoUser
        fields = ['username', 'password1', 'password2']


class ReflectionForm(forms.ModelForm):
    class Meta:
        model = Reflection
        fields = (
            'title',
            'description',
        )
        labels = {
            "title": _("Reflection Title"),
            "description": _("Reflection Text"),
        }
        widgets = {
            'description': forms.Textarea(attrs={"rows": "4"}),
        }


class QuestForm(forms.ModelForm):
    class Meta:
        model = Quest
        fields = {
            'name',
            'description',
        }
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea(attrs={"rows": "4", "placeholder": "Quest Description"}),
        }

    field_order = ['name', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(QuestForm, self).__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return

        if not self.user: raise ValidationError("No user is provided")

        quest_name = self.cleaned_data.get('name')
        if Quest.objects.filter(user=self.user, name=quest_name).exists():
            raise ValidationError("Quest with that name already exists")


class QuestCompletionForm(forms.Form):
    quest_name = forms.CharField()
    complete = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(QuestCompletionForm, self).__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return

        if not self.user: raise ValidationError("No user is provided")

        quest_name = self.cleaned_data.get('quest_name')
        if not Quest.objects.filter(user=self.user, name=quest_name).exists():
            raise ValidationError("Quest do not exists")


def raise_error_if_name_duplicates(error_msg1, error_msg2, forms_list,
                                   obj_class, user=None, name="name", check_in_db=True):
    datas = set()
    for form in forms_list:
        data = form.cleaned_data.get(name)
        if data in datas:
            raise ValidationError(error_msg1)
        datas.add(data)

    if not check_in_db: return

    for data in datas:
        if obj_class.objects.filter(user=user, name=data).exists():
            raise ValidationError(error_msg2.format(data))

### Title Form, Formset, formset_factory ###
class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = (
            'name',
            'description',
        )


class BaseTitleFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseTitleFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return

        raise_error_if_name_duplicates("Titles in a set must have distinct names.",
                                       'Title with name "{}" already exists',
                                       self.forms, Title, user=self.user)


TitleFormSet = modelformset_factory(
    Title,
    TitleForm,
    formset=BaseTitleFormSet,
    extra=0,
    widgets={
        'name': forms.TextInput(attrs={"placeholder": "Title Name"}),
        'description': forms.Textarea(attrs={"placeholder": "Title Description"}),
    },
)


### Job Form, Formset, formset_factory ###
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            'name',
            'description',
        )


class BaseJobFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseJobFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return

        raise_error_if_name_duplicates("Jobs in a set must have distinct names.",
                                       'Job with name "{}" already exists',
                                       self.forms, Job, user=self.user)


JobFormSet = modelformset_factory(
    Job,
    JobForm,
    formset=BaseJobFormSet,
    extra=0,
    widgets={
        'name': forms.TextInput(attrs={"placeholder": "Job Name"}),
        'description': forms.Textarea(attrs={"placeholder": "Job Description"}),
    },
)


### Skill Form, Formset, formset_factory ###
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = (
            'name',
            'description',
            'active',
        )


class BaseSkillFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseSkillFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return

        raise_error_if_name_duplicates("Skills in a set must have distinct names.",
                                       'Skill with name "{}" already exists',
                                       self.forms, Skill, user=self.user)


SkillFormSet = modelformset_factory(
    Skill,
    SkillForm,
    formset=BaseSkillFormSet,
    extra=0,
    widgets={
        'name': forms.TextInput(attrs={"placeholder": "Skill Name"}),
        'description': forms.Textarea(attrs={"placeholder": "Skill Description"}),
        'active': forms.CheckboxInput(attrs={"value": "active"}),
    },
)


### Level Form, Formset, formset_factory ###
class LevelForm(forms.Form):
    skill_name = forms.ChoiceField()
    increase = forms.IntegerField(min_value=1)

    @classmethod
    def set_skill_choices(cls, user):
        skill_choices = ()

        for skill in Skill.objects.filter(user=user):
            skill_value = ((skill.name, f'{skill.name}: {skill.level}'),)
            skill_choices += skill_value
        cls.base_fields["skill_name"].choices = skill_choices


class BaseLevelFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseLevelFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return

        raise_error_if_name_duplicates("Skills in a set must have distinct names.",
                                       "", self.forms, Skill, user=self.user, name="skill_name",
                                       check_in_db=False)


def setup_level_formset(post_data, user, prefix=''):
    LevelForm.set_skill_choices(user)
    LevelFormSet = formset_factory(LevelForm, formset=BaseLevelFormSet)
    return LevelFormSet(post_data, user=user, prefix=prefix)


### Stats Form ###
class StatsForm(forms.Form):
    frontend_incr = forms.IntegerField(min_value=0, label="Frontend", initial=0)
    backend_incr = forms.IntegerField(min_value=0, label="Backend", initial=0)
    data_science_incr = forms.IntegerField(min_value=0, label="Data Science", initial=0)
    data_base_incr = forms.IntegerField(min_value=0, label="Data Bases", initial=0)


### Language Form, Formset, formset_factory ###
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = (
            'name',
            'comprehension',
        )


class BaseLanguageFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseLanguageFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return

        raise_error_if_name_duplicates("Languages in a set must have distinct names.",
                                       'Language with name "{}" already exists',
                                       self.forms, Language, user=self.user)


LanguageFormSet = modelformset_factory(
    Language,
    LanguageForm,
    formset=BaseLanguageFormSet,
    extra=0,
    widgets={
        'name': forms.TextInput(),
        'comprehension': forms.NumberInput(attrs={"min": "0", "max": "100", "step": "0.1"}),
    }
)


### Increase Language Form, Formset, formset_factory ###
class LanguageComprehensionForm(forms.Form):
    lang_name = forms.ChoiceField()
    increase = forms.FloatField(min_value=0, max_value=100, widget=forms.NumberInput(attrs={"step": "0.1"}))

    @classmethod
    def set_language_choices(cls, user):
        lang_choices = ()

        for lang in Language.objects.filter(user=user):
            lang_value = ((lang.name, f'{lang.name}: {lang.comprehension}%'),)
            lang_choices += lang_value
        cls.base_fields["lang_name"].choices = lang_choices


class BaseLanguageIncrFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        raise_error_if_name_duplicates("Languages in a set must have distinct names.",
                                       "", self.forms, Language, name="lang_name",
                                       check_in_db=False)


def setup_language_comprehension_formset(post_data, user, prefix=''):
    LanguageComprehensionForm.set_language_choices(user)
    LanguageComprehensionFormSet = formset_factory(LanguageComprehensionForm, formset=BaseLanguageIncrFormSet)
    return LanguageComprehensionFormSet(post_data, prefix=prefix)


### Description form ###
class DescriptionForm(forms.Form):
    description = forms.CharField(min_length=1, max_length=5110, widget=forms.Textarea())

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .models import TypeAttack, Weapon, ExpPoints, \
    Skill, UserSkills, SkillsRelation, Importer, HelperImporter
import csv
from django.core.files.storage import FileSystemStorage


def download_three(request):
    """Скачать дерево скиллов"""
    csv_writer(request=request)
    three = Importer.objects.get(owner=request.user)
    path = three.file[9:]
    x = HelperImporter.objects.get_or_create(obj=three, file=path)
    return redirect(x[0].file.url)


def check_relations(my_ready_skills, new_skill, parent_scill):
    """
    Проверяет зависимость "new_skill" перед тем, как выучить
    """

    many_relations = set()
    relations = SkillsRelation.objects.filter(child=new_skill)
    if len(relations) == 1 and parent_scill.skill == relations[0].parent:
        # Возвращает тру(всё ок, если зависимость одна)
        return True
    elif len(relations) > 1:
        # Возвращает тру(всё ок, если зависимостей много)
        for rel in relations:
            many_relations.add(rel.parent)
        if many_relations.issubset(my_ready_skills):
            return True


def check_skill_for_learn(request, new_skill):
    """
    Проверяет, можно ли выучить "new_skill"
    """
    my_ready_skills = set()
    my_skills = UserSkills.objects.filter(owner=request.user)
    if new_skill.level > 1:
        for skill in my_skills:
            my_ready_skills.add(skill.skill)
            if check_relations(my_ready_skills=my_ready_skills,
                               new_skill=new_skill,
                               parent_scill=skill):
                return True
            else:
                continue
    else:
        return True


def get_set_for_check(parent_skill, parent_skill_set, ready_skills):
    """
    Возвращает множество скиллов, готовых к изучению.
    """
    many_relations = set()
    relations = SkillsRelation.objects.filter(parent=parent_skill)
    for rel in relations:
        if rel.child not in parent_skill_set and len(SkillsRelation.objects.filter(child=rel.child)) == 1:
            ready_skills.add(rel.child)
        elif len(SkillsRelation.objects.filter(child=rel.child)) > 1:
            child_relations = SkillsRelation.objects.filter(child=rel.child)
            for rel in child_relations:
                many_relations.add(rel.parent)
            if many_relations.issubset(parent_skill_set):
                ready_skills.add(rel.child)
    return ready_skills


def check_available_skills(request):
    """Проверить, какие скиллы можно изучить, а какие нельзя"""
    skill_list, ready_skills, no_study = set(), set(), set()

    my_skills = UserSkills.objects.filter(owner=request.user)
    for skill in my_skills:
        skill_list.add(skill.skill)

    all_skills = Skill.objects.all()
    for skill in all_skills:
        if skill in skill_list:
            get_ready_skills = get_set_for_check(parent_skill=skill,
                                                 parent_skill_set=skill_list,
                                                 ready_skills=ready_skills)
            ready_skills.update(get_ready_skills)
        elif skill.level == 1:
            ready_skills.add(skill)
        else:
            no_study.add(skill)

    no_ready_skills = no_study - ready_skills

    return skill_list, ready_skills, no_ready_skills


def give_exp(request, skill):
    """
    Отнимает Exp у пользователя и возвращает True или возаращает False
    """
    price = skill.cost
    exp_points = ExpPoints.objects.get(owner=request.user)
    if exp_points.quantity >= price:
        exp_points.quantity -= price
        exp_points.save()
        return True
    else:
        return False


def skill_up(request, skill):
    new_skill = UserSkills.objects.filter(skill=skill)
    if not new_skill and give_exp(request=request, skill=skill):
        UserSkills.objects.create(owner=request.user, skill=skill, activate=True,
                                  level=1, damage=skill.damage)


def skill_upgrade(skill):
    skill_up = UserSkills.objects.get(skill=skill)
    skill_up = SkillUpdater(skill_up)
    skill_up.skill_upgrade()


class SkillUpdater:

    def __init__(self, skill: UserSkills):
        self.me = skill

    def skill_upgrade(self, level_up=1):
        self.me.level += int(level_up)
        self.me.damage = (self.me.level * 2.1) + self.me.damage
        return self.me.save()


def skills(request):
    """
    Главная страница скиллов
    """
    # Если не авторизован
    if not request.user.is_authenticated:
        return redirect('login')
    # Проверяем скиллы, готовые к изучению
    skill_list, ready_skills, no_ready_skills = check_available_skills(request=request)
    # csv_importer(request=request)


    # Сортируем типы атаки для html
    types_attacks = TypeAttack.objects.all()
    skills = Skill.objects.all()
    my_skills = UserSkills.objects.filter(owner=request.user)
    weapons = Weapon.objects.all()
    exp_points = ExpPoints.objects.filter(owner=request.user)
    skill_relation = SkillsRelation.objects.all()

    if exp_points:
        exp_points = exp_points[0]
    else:
        ExpPoints.objects.create(owner=request.user, quantity=0)

    context = {
        'types_attacks': types_attacks,
        # range нужен для html, чтобы сделать цикл от 1 до 4 (с 1 по максимальный уровень скилла)
        'range': range(1, 5),
        'skills': skills,
        'my_skills': my_skills,
        'weapons': weapons,

        'skill_list': skill_list,
        'ready_skills': ready_skills,
        'no_ready_skills': no_ready_skills,
        'skill_relations': skill_relation,

        'exp_points': exp_points
    }

    if request.method == 'GET':
        if 'skill' in request.GET:
            skill = Skill.objects.get(skill_name=request.GET['skill'])
            # Если прошли проверку и скилл можно учить:
            if check_skill_for_learn(request=request, new_skill=skill):
                # Учим скилл
                skill_up(request=request, skill=skill)
                # Редиректим на главную
                return redirect('skills')
        elif 'skill_upgrade' in request.GET:
            skill = Skill.objects.get(skill_name=request.GET['skill_upgrade'])
            if give_exp(request=request, skill=skill):
                skill_upgrade(skill=skill)
                return redirect('skills')
            else:
                return redirect('skills')
        elif 'delete' in request.GET:
            # Удалить ветку скиллов пользователя (для проверки импорта/экспорта)
            UserSkills.objects.filter(owner=request.user).delete()
            return redirect('skills')
    # Загруженный файл, в MEDIA_ROOT (сейчас это pictures) принимаем через POST
    if request.method == 'POST':
        # Находим файл
        file = request.FILES['export']
        fs = FileSystemStorage()
        # Сохраняем в MEDIA_ROOT
        name = fs.save(file.name, file)
        url = fs.path(name)
        # Вкачиваем скиллы
        csv_importer(file=url, request=request)

    return render(request, 'skills/general.html', context)


def ajax_form(request):
    """Добавляем Exp через Ajax"""
    if request.GET:
        if 'exp' in request.GET:
            test = request.GET['exp']
            if '+5 exp' in test:
                exp_points = ExpPoints.objects.get(owner=request.user)
                exp_points.quantity += 5
                exp_points.save()
                return HttpResponse(f"{exp_points.quantity}")
            else:
                return HttpResponse("no", content_type='text/html')
    else:
        return HttpResponse("no", content_type='text/html')


def csv_writer(request):
    """Импортирует вкаченные скиллы пользователя в csv"""
    field_names = ['activate', 'owner_id', 'skill_id', 'level', 'damage']
    content = []
    filename = f'Ветка-скиллов-{request.user}'
    my_skills = UserSkills.objects.filter(owner=request.user)
    for skill in my_skills:
        content.append({'activate': skill.activate,
                          'owner_id': skill.owner_id,
                          'skill_id': skill.skill_id,
                          'level': skill.level,
                          'damage': skill.damage})

    with open(f'pictures/skill_image/{filename}.csv', 'w', newline='') as out_csv:
        writer = csv.DictWriter(out_csv, delimiter=',', fieldnames=field_names)
        writer.writeheader()
        writer.writerows(content)
    # Создаёт модель Importer (Там в атрибуте file хранится путь к созданному csv)
    Importer.objects.get_or_create(name=filename, owner=request.user, file=f'pictures/skill_image/{filename}.csv')


def csv_importer(file, request):
    """Вкачивает скиллы из импортированного csv"""
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')  # <csv.DictReader object at 0x03B11030>
        for row in reader:
            activate = row['activate']
            skill_id = row['skill_id']
            level = row['level']
            damage = row['damage']

            UserSkills.objects.get_or_create(activate=activate,
                                      owner=request.user,
                                      skill_id=skill_id,
                                      level=level,
                                      damage=damage)

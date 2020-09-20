from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TypeAttack(models.Model):
    """Тип атаки"""
    type = models.CharField('Тип атаки', max_length=100)

    def __str__(self):
        return self.type


class Weapon(models.Model):
    """Оружие"""
    weapon_name = models.CharField('Оружие', max_length=100)
    category = models.ForeignKey(TypeAttack, on_delete=models.CASCADE, null=True)
    img = models.ImageField(default='no-image.png', upload_to='skill_image')

    def __str__(self):
        return f'{self.weapon_name}'


class ExpPoints(models.Model):
    """Очки опыта"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.owner} - {self.quantity}'


class Skill(models.Model):
    """Навык"""
    skill_name = models.CharField('Название', max_length=100)
    description = models.TextField()
    img = models.ImageField(default='no-image.png', upload_to='skill_image')
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, null=True)
    level = models.IntegerField(null=True)
    damage = models.IntegerField(null=True)
    cost = models.IntegerField(verbose_name='Стоимость', null=True)

    def __str__(self):
        return f'{self.skill_name}'


class UserSkills(models.Model):
    """Навык пользователя"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)
    damage = models.IntegerField(null=True)
    activate = models.BooleanField(default=False)
    level = models.IntegerField(verbose_name='Уровень скилла', null=True)

    def __str__(self):
        return f'{self.skill} - {self.owner} - {self.level}'


class SkillsRelation(models.Model):
    """Зависимость навыков"""
    child = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, related_name='higher')
    parent = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'child={self.child} parent={self.parent}'


class Importer(models.Model):
    name = models.CharField(verbose_name='Название файла', max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    file = models.FilePathField(path='pictures/skill_image/')
    def __str__(self):
        return f'{self.name}'


class HelperImporter(models.Model):
    obj = models.ForeignKey(Importer, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='skill_image')

    def __str__(self):
        return f'{self.obj}'

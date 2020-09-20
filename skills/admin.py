from django.contrib import admin
from .models import TypeAttack, Weapon, ExpPoints, Skill, \
    UserSkills, SkillsRelation, Importer, HelperImporter

admin.site.register(TypeAttack)
admin.site.register(Weapon)
admin.site.register(ExpPoints)
admin.site.register(Skill)
admin.site.register(UserSkills)
admin.site.register(SkillsRelation)
admin.site.register(Importer)
admin.site.register(HelperImporter)

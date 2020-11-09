from django.db import models
from django.contrib.postgres.fields import ArrayField
from project.utils.models import User

ALIGNMENTS = [
    ('chaotic_good', 'Chaotic Good'),
]

EXP_TO_LEVEL = [

]

ABILITIES = [
    ('str', 'Strength'),
    ('dex', 'Dexterity'),
    ('con', 'Constitution'),
    ('int', 'Intelligence'),
    ('wis', 'Wisdom'),
    ('cha', 'Charisma'),
]

SKILLS = [
    ('athletics', 'Athletics'),
]

ABILITIES_TO_SKILLS = {

}

LANGUAGES = [
    ('dwarvish', 'Dwarvish'),
]

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    dungeon_master = models.ForeignKey(User, related_name="dm_campaigns", on_delete=models.CASCADE)
    

class Character(models.Model):
    campaign = models.ForeignKey(Campaign, related_name="characters", on_delete=models.CASCADE)
    player = models.ForeignKey(User, related_name="characters", on_delete=models.CASCADE)
    exp_points = models.IntegerField(default=0)
    alignment = models.CharField(max_length=50, choices=ALIGNMENTS)
    str_score = models.IntegerField(default=10)
    dex_score = models.IntegerField(default=10)
    con_score = models.IntegerField(default=10)
    int_score = models.IntegerField(default=10)
    wis_score = models.IntegerField(default=10)
    cha_score = models.IntegerField(default=10)
    saving_throw_prof = ArrayField(models.CharField(max_length=50, choices=ABILITIES))
    skill_prof = ArrayField(models.CharField(max_length=50, choices=SKILLS), default=list)
    skill_expert = ArrayField(models.CharField(max_length=50, choices=SKILLS), default=list)
    tool_proficiencies = TextField(null=True, blank=True)
    languages = ArrayField(models.CharField(max_length=50, choices=LANGUAGES), default=list)
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=20)
    height = models.CharField(max_length=10)
    weight = models.IntegerField(default=100)
    appearance = models.TextField(null=True, blank=True)
    personality_traits = models.TextField(null=True, blank=True)
    ideals = models.TextField(null=True, blank=True)
    bonds = models.TextField(null=True, blank=True)
    flaws = models.TextField(null=True, blank=True)
    background_story = models.TextField(null=True, blank=True)
    hit_points_max = models.IntegerField(default=6)
    current_hit_points = models.IntegerField(default=6)
    hit_dice_max = models.CharField(max_length=10)
    current_hit_dice = models.CharField(max_length=10)
    inspiration = models.IntegerField(default=0)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    classes = models.ManyToManyField(DnDClass)
    backpack = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    arsenal = models.ForeignKey(Arsenal, on_delete=models.CASCADE)
    spellbook = models.ForeignKey(Spellbook, on_delete=models.CASCADE)

    @property
    def level(self):
        pass

    @property
    def str_mod(self):
        pass

    @property
    def dex_mod(self):
        pass

    @property
    def con_mod(self):
        pass

    @property
    def wis_mod(self):
        pass

    @property
    def int_mod(self):
        pass

    @property
    def cha_mod(self):
        pass

    @property
    def initiative(self):
        pass

    @property
    def passive_perception(self):
        pass

    def skill_mod(self, skill):
        pass

class Race(models.Model):
    pass

class DnDClass(models.Model):
    pass

class Background(models.Model):
    pass

class Inventory(models.Model):
    pass

class Wallet(models.Model):
    pass

class Arsenal(models.Model):
    weapons = models.ManyToManyField(Weapon)

class Weapon(models.Model):
    pass

class Spellbook(models.Model):
    spells = models.ManyToManyField(Spell)

class Spell(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    

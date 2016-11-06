from django.core.exceptions import ValidationError
from django.test import TestCase

from idm_core.models import Person
from idm_core.name.models import Name


class NamesTestCase(TestCase):
    fixtures = ['initial']

    def testMononym(self):
        person = Person.objects.create()
        name = Name(person=person,
                    components=[{'type': 'mononym', 'value': 'Socrates'}])
        name.save()
        self.assertEqual(str(name), 'Socrates')
        self.assertEqual(name.plain, 'Socrates')
        self.assertEqual(name.plain_full, 'Socrates')
        self.assertEqual(name.familiar, 'Socrates')
        self.assertEqual(name.sort, 'Socrates')
        self.assertEqual(name.marked_up, '<name><mononym>Socrates</mononym></name>')

    def testMultipleMononyms(self):
        person = Person.objects.create()
        name = Name(person=person,
                    components=[{'type': 'mononym', 'value': 'Socrates'},
                                {'type': 'mononym', 'value': 'Socrates'}])
        with self.assertRaises(ValidationError):
            name.save()

    def testWestern(self):
        person = Person.objects.create()
        name = Name(person=person,
                    components=[{'type': 'prefix', 'value': 'Rear Admiral'},
                                {'type': 'given', 'value': 'Grace'},
                                {'type': 'middle', 'value': 'Brewster'},
                                {'type': 'middle', 'value': 'Murray'},
                                {'type': 'family', 'value': 'Hopper'}])
        name.save()
        self.assertEqual(str(name), 'Rear Admiral Grace Brewster Murray Hopper')
        self.assertEqual(name.plain, 'Grace Hopper')
        self.assertEqual(name.plain_full, 'Rear Admiral Grace Brewster Murray Hopper')
        self.assertEqual(name.familiar, 'Grace')
        self.assertEqual(name.sort, 'Hopper, Grace Brewster Murray')
        self.assertEqual(name.marked_up,
                         '<name><prefix>Rear Admiral</prefix> <given>Grace</given> <middle>Brewster</middle> '
                         '<middle>Murray</middle> <family>Hopper</family></name>')

    def testChinese(self):
        person = Person.objects.create()
        name = Name(person=person,
                    space_delimited=False,
                    components=[{'type': 'family', 'value': '夏侯'},
                                {'type': 'given', 'value': '徽'}])
        name.save()
        self.assertEqual(str(name), '夏侯徽')
        self.assertEqual(name.plain, '夏侯徽')
        self.assertEqual(name.plain_full, '夏侯徽')
        self.assertEqual(name.familiar, '徽')
        self.assertEqual(name.sort, '夏侯徽')
        self.assertEqual(name.marked_up, '<name><family>夏侯</family><given>徽</given></name>')

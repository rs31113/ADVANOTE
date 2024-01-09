import django.test

import notes.models
import tag.models
import users.models


class CreateNoteTests(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = users.models.User.objects.create_user(
            "Max",
            "neverov@gmail.com",
            "123RTYdfd222",
        )
        cls.tag = tag.models.Tag.objects.create(
            name="Tag Test",
        )

    def test_create_note(self):
        note_count = notes.models.Note.objects.count()
        notes.models.Note.objects.create(
            owner=self.user,
            text="Test text!",
        )
        self.assertEqual(note_count + 1, notes.models.Note.objects.count())

    def test_owner_note(self):
        notes.models.Note.objects.create(
            title="Title!",
            owner=self.user,
            text="Test text!",
        )
        note = notes.models.Note.objects.get(id=1)

        with self.subTest():
            self.assertEqual(note.owner, self.user)

    def test_text_note(self):
        notes.models.Note.objects.create(
            title="Title!",
            owner=self.user,
            text="Test text!",
        )
        note = notes.models.Note.objects.get(id=1)

        with self.subTest():
            self.assertEqual(note.text, "Test text!")

    def test_title_note(self):
        notes.models.Note.objects.create(
            title="Title!",
            owner=self.user,
            text="Test text!",
        )
        note = notes.models.Note.objects.get(id=1)

        with self.subTest():
            self.assertEqual(note.title, "Title!")

    def test_note(self):
        note_count = notes.models.Note.objects.count()
        notes.models.Note.objects.create(
            title="Title!",
            owner=self.user,
            text="Test text!",
        )
        other_user = users.models.User.objects.create_user(
            "NoMax",
            "NOneverov@gmail.com",
            "123RTYdfd222",
        )
        notes.models.Note.objects.create(
            title="Title!",
            owner=other_user,
            text="Test text!",
        )
        self.assertEqual(note_count + 2, notes.models.Note.objects.count())

    def test_tag_with_note(self):
        notes.models.Note.objects.create(
            title="Title!",
            owner=self.user,
            text="Test text!",
        )
        note = notes.models.Note.objects.get(id=1)
        note.tags.add(self.tag)

        with self.subTest(tags=note.tags.all()):
            self.assertEqual(note.tags.all().first(), self.tag)

    def test_many_tag_with_note(self):
        notes.models.Note.objects.create(
            title="Title!",
            owner=self.user,
            text="Test text!",
        )

        note = notes.models.Note.objects.get(id=1)
        self.tag1 = tag.models.Tag.objects.create(
            name="Tag Test 1",
        )
        note.tags.add(self.tag)
        note.tags.add(self.tag1)

        with self.subTest(tags=note.tags.all()):
            self.assertEqual(note.tags.all().first(), self.tag)
            self.assertEqual(note.tags.all()[1], self.tag1)


__all__ = ()

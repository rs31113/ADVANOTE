import django.db
import django.test

import tag.models


class CreateTagTests(django.test.TestCase):
    def test_create_tag(self):
        count_tag = tag.models.Tag.objects.count()
        tag.models.Tag.objects.create(
            name="Test tag",
        )
        self.assertEqual(count_tag + 1, tag.models.Tag.objects.count())

    def test_name_tag(self):
        tag.models.Tag.objects.create(
            name="Test tag",
        )
        tags = tag.models.Tag.objects.get(id=1)
        with self.subTest(tag=tags):
            self.assertEqual(tags.name, "Test tag")

    def test_error_tag_name_unique(self):
        tag.models.Tag.objects.create(
            name="Test tag",
        )
        with self.assertRaises(django.db.IntegrityError):
            tag.models.Tag.objects.create(
                name="Test tag",
            )


__all__ = ()

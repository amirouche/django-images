import os
from json import dumps

from django.conf import settings
from django.test import TestCase
from django.core.files.storage import default_storage
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import InMemoryUploadedFile

from django_images.models import Image
from django_images.forms import ImageForm
from django_images.forms import MultipleFormatImageForm

from .models import TestImage


class TestDjangoImages(TestCase):

    def test_validation(self):
        """Validate an image against a complex format"""
        filepath = os.path.join(settings.BASE_DIR, 'middle.jpeg')

        with open(filepath) as f:
            # prepare form data
            image = InMemoryUploadedFile(
                f,
                'image',
                'middle.jpeg',
                'image/jpeg',
                42,  # not significant for the test
                'utf-8'
            )
            files = MultiValueDict()
            files['image'] = image
            post = MultiValueDict()
            post['name'] = 'test image'
            # create form
            form = ImageForm(TestImage, post, files)
            # validate resize operation
            v = form.is_valid()
            self.assertTrue(v)

    def test_multi_format_validation(self):
        """Validate an image against a complex format"""
        filepath = os.path.join(settings.BASE_DIR, 'big.jpeg')

        with open(filepath) as f:
            # prepare form data
            image = InMemoryUploadedFile(
                f,
                'image',
                'big.jpeg',
                'image/jpeg',
                42,  # not significant for the test
                'utf-8'
            )
            files = MultiValueDict()
            files['image'] = image
            post = MultiValueDict()
            post['name'] = 'test image'
            post['fmt'] = 'TestImage'
            # create form
            form = MultipleFormatImageForm(Image.formats(), post, files)
            # validate resize operation
            v = form.is_valid()
            self.assertTrue(v)

    def test_resize_big_image_in_background_format(self):
        """Test resizing of big enough image to background format"""
        filepath = os.path.join(settings.BASE_DIR, 'big.jpeg')

        with open(filepath) as f:
            # prepare form data
            image = InMemoryUploadedFile(
                f,
                'image',
                'big.jpeg',
                'image/jpeg',
                42,  # not significant for the test
                'utf-8'
            )
            files = MultiValueDict()
            files['image'] = image
            post = MultiValueDict()
            post['name'] = 'test image'
            # create form
            form = ImageForm(TestImage, post, files)
            # validate resize operation
            self.assertTrue(form.is_valid())

            # execute resize operation
            image = form.save()

            for size in ('og', 'lg', 'md', 'sm', 'xs'):
                filepath = getattr(image, size)['filepath']
                filepath = os.path.join(settings.MEDIA_ROOT, filepath)
                self.assertTrue(os.path.exists(filepath))

    def test_model_api(self):
        """Test that Image model behave correctly"""
        image = TestImage(
            uid='42',
            json_xs=dumps(dict(
                width=100,
                height=100,
                filepath='42_xs.ext',
            )),
            json_sm=dumps(dict(
                width=100,
                height=100,
                filepath='42_sm.ext',
            )),
            json_md=dumps(dict(
                width=100,
                height=100,
                filepath='42_md.ext',
            )),
            json_lg=dumps(dict(
                width=100,
                height=100,
                filepath='42_lg.ext',
            )),
            json_og=dumps(dict(
                width=100,
                height=100,
                filepath='42.ext',
            ))
        )

        self.assertEqual(
            image.xs['url'],
            'http://example.com/media/42_xs.ext'
        )
        self.assertEqual(
            image.sm['url'],
            'http://example.com/media/42_sm.ext'
        )
        self.assertEqual(
            image.md['url'],
            'http://example.com/media/42_md.ext'
        )
        self.assertEqual(
            image.lg['url'],
            'http://example.com/media/42_lg.ext'
        )
        self.assertEqual(
            image.og['url'],
            'http://example.com/media/42.ext'
        )

    def test_fail_to_resize_small_image_in_background_format(self):
        """Test resizing of image fails validation"""
        filepath = os.path.join(settings.BASE_DIR, 'small.jpeg')

        with open(filepath) as f:
            # prepare form data
            image = InMemoryUploadedFile(
                f,
                'image',
                'small.jpeg',
                'image/jpeg',
                42,  # not significant for the test
                'utf-8'
            )
            files = MultiValueDict()
            files['image'] = image
            post = MultiValueDict()
            post['ptype'] = 1
            post['name'] = 'test with small.jpeg'

            # create form
            form = ImageForm(TestImage, post, files)

            # validate resize operation
            self.assertFalse(form.is_valid())

    def test_generate_unique_filename(self):
        """Test that two images with same size and same name
        can be stored on disk"""
        def create_image():
            filepath = os.path.join(settings.BASE_DIR, 'big.jpeg')
            with open(filepath) as f:
                # prepare form data
                image = InMemoryUploadedFile(
                    f,
                    'image',
                    'big.jpeg',
                    'image/jpeg',
                    42,  # not significant for the test
                    'utf-8'
                )
                files = MultiValueDict()
                files['image'] = image
                post = MultiValueDict()
                post['name'] = 'test image'
                # create form
                form = ImageForm(TestImage, post, files)
                # validate resize operation
                form.is_valid()

                # execute resize operation
                image = form.save()
                return image
        # create two times the same image:
        one = create_image()
        two = create_image()
        self.assertTrue(one.og['url'] != two.og['url'])

    def test_delete_image(self):
        """Test that two images with same size and same name
        can be stored on disk"""
        def create_image():
            filepath = os.path.join(settings.BASE_DIR, 'big.jpeg')
            with open(filepath) as f:
                # prepare form data
                image = InMemoryUploadedFile(
                    f,
                    'image',
                    'big.jpeg',
                    'image/jpeg',
                    42,  # not significant for the test
                    'utf-8'
                )
                files = MultiValueDict()
                files['image'] = image
                post = MultiValueDict()
                post['ptype'] = 1
                post['name'] = 'test with big.jpeg'

                # create form
                form = ImageForm(TestImage, post, files)
                # validate resize operation
                form.is_valid()

                # execute resize operation
                image = form.save()
                return image
        # create two times the same image:
        one = create_image()
        self.assertTrue(default_storage.exists(one.og['filepath']))
        one.delete()
        self.assertFalse(default_storage.exists(one.og['filepath']))

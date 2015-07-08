import os
from django.test import TestCase

from django.conf import settings
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import InMemoryUploadedFile

from django_images.image import save
from django_images.forms import ImageForm
from django_images.forms import ImageFixedFormatForm


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
            post['ptype'] = 5
            post['name'] = 'test with middle.jpeg'

            # create form
            form = ImageForm(post, files)
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
            post['ptype'] = 1
            post['name'] = 'test with big.jpeg'

            # create form
            form = ImageForm(post, files)
            # validate resize operation
            self.assertTrue(form.is_valid())

            # execute resize operation
            data = form.cleaned_data
            filename = slugify(data['name'])
            image = save(data['image'], filename, data['ptype'])

            for size in ('og', 'lg', 'md', 'sm', 'xs'):
                filepath = image.relativeurl(size)
                filepath = os.path.join(settings.MEDIA_ROOT, filepath)
                self.assertTrue(os.path.exists(filepath))

    def test_form_fixed_format_form(self):
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

            # create form
            form = ImageFixedFormatForm('1', 'test', post, files)

            # validate resize operation
            self.assertTrue(form.is_valid())

            # execute resize operation
            data = form.cleaned_data
            filename = slugify(form.name)
            image = save(data['image'], filename, form.ptype)

            for size in ('og', 'lg', 'md', 'sm', 'xs'):
                filepath = image.relativeurl(size)
                filepath = os.path.join(settings.MEDIA_ROOT, filepath)
                self.assertTrue(os.path.exists(filepath))

    def test_model_api(self):
        """Test that Image model behave correctly"""
        from django_images.models import Image
        image = Image(
            ptype='1',
            name='test image model',
            uid='42',
            ext='ext',
            xs_width=100,
            xs_height=100,
            sm_width=200,
            sm_height=200,
            md_width=300,
            md_height=300,
            lg_width=400,
            lg_height=400,
            og_width=1000,
            og_height=1000,
        )
        self.assertEqual(
            image.xs['url'],
            'http://example.com/media/covers/42_100x100.ext'
        )
        self.assertEqual(
            image.sm['url'],
            'http://example.com/media/covers/42_200x200.ext'
        )
        self.assertEqual(
            image.md['url'],
            'http://example.com/media/covers/42_300x300.ext'
        )
        self.assertEqual(
            image.lg['url'],
            'http://example.com/media/covers/42_400x400.ext'
        )
        self.assertEqual(
            image.og['url'],
            'http://example.com/media/covers/42_1000x1000.ext'
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
            form = ImageForm(post, files)

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
                post['ptype'] = 1
                post['name'] = 'test with big.jpeg'

                # create form
                form = ImageForm(post, files)
                # validate resize operation
                form.is_valid()

                # execute resize operation
                data = form.cleaned_data
                filename = slugify(data['name'])
                image = save(data['image'], filename, data['ptype'])
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
                form = ImageForm(post, files)
                # validate resize operation
                form.is_valid()

                # execute resize operation
                data = form.cleaned_data
                filename = slugify(data['name'])
                image = save(data['image'], filename, data['ptype'])
                return image
        # create two times the same image:
        one = create_image()
        self.assertTrue(default_storage.exists(one.relativeurl('og')))
        one.delete()
        self.assertFalse(default_storage.exists(one.relativeurl('og')))

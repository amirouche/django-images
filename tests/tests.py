import os
from django.test import TestCase

from django.conf import settings
from django.utils.text import slugify
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import InMemoryUploadedFile

from django_images.pictt import save
from django_images.forms import PictureForm
from django_images.forms import PictureFixedFormatForm


class TestDjangoImages(TestCase):

    def test_resize_big_image_in_background_format(self):
        """Test resizing of big enough image to background format"""
        filepath = os.path.join(settings.BASE_DIR, 'big.jpeg')

        with open(filepath) as f:
            # prepare form data
            image = InMemoryUploadedFile(
                f,
                'picture',
                'big.jpeg',
                'image/jpeg',
                42,  # not significant for the test
                'utf-8'
            )
            files = MultiValueDict()
            files['picture'] = image
            post = MultiValueDict()
            post['ptype'] = 1
            post['name'] = 'test with big.jpeg'

            # create form
            form = PictureForm(post, files)
            # validate resize operation
            self.assertTrue(form.is_valid())

            # execute resize operation
            data = form.cleaned_data
            filename = slugify(data['name'])
            picture = save(data['picture'], filename, data['ptype'])

            for size in ('og', 'lg', 'md', 'sm', 'xs'):
                filepath = picture.relativeurl(size)
                filepath = os.path.join(settings.MEDIA_ROOT, filepath)
                self.assertTrue(os.path.exists(filepath))

    def test_form_fixed_format_form(self):
        """Test resizing of big enough image to background format"""
        filepath = os.path.join(settings.BASE_DIR, 'big.jpeg')

        with open(filepath) as f:
            # prepare form data
            image = InMemoryUploadedFile(
                f,
                'picture',
                'big.jpeg',
                'image/jpeg',
                42,  # not significant for the test
                'utf-8'
            )
            files = MultiValueDict()
            files['picture'] = image
            post = MultiValueDict()

            # create form
            form = PictureFixedFormatForm('1', 'test', post, files)

            # validate resize operation
            self.assertTrue(form.is_valid())

            # execute resize operation
            data = form.cleaned_data
            filename = slugify(form.name)
            picture = save(data['picture'], filename, form.ptype)

            for size in ('og', 'lg', 'md', 'sm', 'xs'):
                filepath = picture.relativeurl(size)
                filepath = os.path.join(settings.MEDIA_ROOT, filepath)
                self.assertTrue(os.path.exists(filepath))

    def test_model_api(self):
        """Test that Picture model behave correctly"""
        from django_images.models import Picture
        picture = Picture(
            ptype='1',
            name='test-picture-model',
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
            picture.xs['url'],
            'http://example.com/media/covers/test-picture-model_100x100.ext'
        )
        self.assertEqual(
            picture.sm['url'],
            'http://example.com/media/covers/test-picture-model_200x200.ext'
        )
        self.assertEqual(
            picture.md['url'],
            'http://example.com/media/covers/test-picture-model_300x300.ext'
        )
        self.assertEqual(
            picture.lg['url'],
            'http://example.com/media/covers/test-picture-model_400x400.ext'
        )
        self.assertEqual(
            picture.og['url'],
            'http://example.com/media/covers/test-picture-model_1000x1000.ext'
        )

    def test_fail_to_resize_small_image_in_background_format(self):
        """Test resizing of image fails validation"""
        filepath = os.path.join(settings.BASE_DIR, 'small.jpeg')

        with open(filepath) as f:
            # prepare form data
            image = InMemoryUploadedFile(
                f,
                'picture',
                'small.jpeg',
                'image/jpeg',
                42,  # not significant for the test
                'utf-8'
            )
            files = MultiValueDict()
            files['picture'] = image
            post = MultiValueDict()
            post['ptype'] = 1
            post['name'] = 'test with small.jpeg'

            # create form
            form = PictureForm(post, files)

            # validate resize operation
            self.assertFalse(form.is_valid())

    def test_generate_unique_filename(self):
        """Test that two images with same size and same name
        can be stored on disk"""
        def create_picture():
            filepath = os.path.join(settings.BASE_DIR, 'big.jpeg')
            with open(filepath) as f:
                # prepare form data
                image = InMemoryUploadedFile(
                    f,
                    'picture',
                    'big.jpeg',
                    'image/jpeg',
                    42,  # not significant for the test
                    'utf-8'
                )
                files = MultiValueDict()
                files['picture'] = image
                post = MultiValueDict()
                post['ptype'] = 1
                post['name'] = 'test with big.jpeg'

                # create form
                form = PictureForm(post, files)
                # validate resize operation
                form.is_valid()

                # execute resize operation
                data = form.cleaned_data
                filename = slugify(data['name'])
                picture = save(data['picture'], filename, data['ptype'])
                return picture
        # create two times the same picture:
        one = create_picture()
        two = create_picture()
        self.assertFalse(one.og['url'] != two.og['url'])

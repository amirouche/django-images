import os
from django.test import TestCase

from django.conf import settings
from django.utils.text import slugify
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import InMemoryUploadedFile

from django_images.forms import PictureForm
from django_images.pictt import save


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
            FILES = MultiValueDict()
            FILES['picture'] = image
            POST = MultiValueDict()
            POST['ptype'] = 1
            POST['name'] = 'test with big.jpeg'

            # create form
            form = PictureForm(POST, FILES)
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
            FILES = MultiValueDict()
            FILES['picture'] = image
            POST = MultiValueDict()
            POST['ptype'] = 1
            POST['name'] = 'test with small.jpeg'

            # create form
            form = PictureForm(POST, FILES)

            # validate resize operation
            self.assertFalse(form.is_valid())

import os
from io import BytesIO

from PIL import Image, ImageCms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), 'resources/')
MASK_WIDTH_PX = 1680
MASK_HEIGHT_PX = 945
MASK_IMAGE_PATH = os.path.join(RESOURCE_DIR, 'mask_image_mask.png')
PROFILE_RGB_ADOBE = os.path.join(RESOURCE_DIR, 'icc_profiles/RGB/AdobeRGB1998.icc')
PROFILE_CMYK_US_WEB_COATED = os.path.join(RESOURCE_DIR, 'icc_profiles/CMYK/USWebCoatedSWOP.icc')


class Facemask(models.Model):
    full_image = models.ImageField(upload_to='facemask/full_image/')
    thumbnail = models.ImageField(upload_to='facemask/thumbnail/', blank=True, null=True)

    mask_image = models.ImageField(upload_to='facemask/mask_image/', blank=True, null=True)

    def get_profile_or_default(self, image: Image.Image) -> ImageCms.ImageCmsProfile:
        input_profile_str = image.info.get('icc_profile')
        if input_profile_str:
            input_profile = BytesIO(input_profile_str)
            return ImageCms.ImageCmsProfile(input_profile)
        else:
            return ImageCms.ImageCmsProfile(PROFILE_RGB_ADOBE)

    def create_mask_image(self, override=False):
        if self.mask_image and not override:
            return False
        full_image = Image.open(self.full_image)
        # Resize
        mask_sized_image = full_image.resize((MASK_WIDTH_PX, MASK_HEIGHT_PX))
        # Apply mask
        mask_image = Image.open(MASK_IMAGE_PATH)
        mask_sized_image.paste(mask_image, (0, 0), mask_image)
        # Profile conversion
        input_profile = self.get_profile_or_default(mask_sized_image)
        mask_sized_image_cmyk = ImageCms.profileToProfile(mask_sized_image, inputProfile=input_profile, outputProfile=PROFILE_CMYK_US_WEB_COATED, outputMode='CMYK')
        # Save to mask_image
        mask_image_buffer = BytesIO()
        mask_sized_image_cmyk.save(fp=mask_image_buffer, format='JPEG')

        mask_image_name = 'mask_image_%s.jpg' % (self.id,)
        self.mask_image = SimpleUploadedFile(mask_image_name, mask_image_buffer.getvalue(), 'image/jpeg')
        self.save()

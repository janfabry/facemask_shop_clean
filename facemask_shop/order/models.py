import os
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from oscar.apps.order.abstract_models import AbstractOrder
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing, Shape, STATE_DEFAULTS
from reportlab.lib import colors
from reportlab.lib.colors import CMYKColorSep
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from svglib.svglib import svg2rlg

from facemask_shop.editor.models import Facemask

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), 'resources/')

FONT_NAME = 'DejaVuSans'

registerFont(TTFont('DejaVuSans', os.path.join(RESOURCE_DIR, 'fonts/DejaVuSans.ttf')))
registerFont(TTFont('DejaVuSans-Bold', os.path.join(RESOURCE_DIR, 'fonts/DejaVuSans-Bold.ttf')))
registerFont(TTFont('DejaVuSans-Oblique', os.path.join(RESOURCE_DIR, 'fonts/DejaVuSans-Oblique.ttf')))
registerFont(TTFont('DejaVuSans-BoldOblique', os.path.join(RESOURCE_DIR, 'fonts/DejaVuSans-BoldOblique.ttf')))
registerFontFamily(FONT_NAME, bold='DejaVuSans-Bold', italic='DejaVuSans-Oblique', boldItalic='DejaVuSans-BoldOblique')

STATE_DEFAULTS['fontName'] = FONT_NAME

PAGE_WIDTH_PT = 805
PAGE_HEIGHT_PT = 490

BLEED_WIDTH_PT = 805
BLEED_HEIGHT_PT = 452

QR_OFFSET_X_PT = 398
QR_OFFSET_Y_PT = 386
QR_SIZE_PT = 75
QR_ROTATION = 42

CUT_COLOR = CMYKColorSep(1, 0.67, 0, 0.23, spotName='cut')
CUTLINE_OFFSET_X_PT = 11
CUTLINE_OFFSET_Y_PT = 15
CUTLINES_PATH = os.path.join(RESOURCE_DIR, 'cutlines.svg')
CUTLINES_DRAWING = svg2rlg(CUTLINES_PATH)


def set_shape_color(groupOrShape: Shape, color):
    if 'contents' in groupOrShape.getProperties():
        for item in groupOrShape.contents:
            set_shape_color(item, color)
    if 'strokeColor' in groupOrShape.getProperties():
        if groupOrShape.strokeColor:
            groupOrShape.strokeColor = color


set_shape_color(CUTLINES_DRAWING, CUT_COLOR)

ORDER_INFO_FONT_SIZE_PT = 13
ORDER_INFO_OFFSET_X_PT = 15
ORDER_INFO_OFFSET_Y_PT = 15

SHIPPING_LABEL_OFFSET_X_PT = 15
SHIPPING_LABEL_OFFSET_Y_PT = 15
SHIPPING_LABEL_WIDTH = 200
SHIPPING_LABEL_STYLE = ParagraphStyle(
    name='ShippingLabel',
    fontName=FONT_NAME,
    fontSize=ORDER_INFO_FONT_SIZE_PT,
    borderColor=CUT_COLOR,
    borderWidth=1,
    borderPadding=10
)

class Order(AbstractOrder):
    print_file = models.FileField(upload_to='orders/', blank=True, null=True)

    def is_open_payment(self):
        return self.status == settings.OSCAR_ORDER_STATUSES.PENDING

    def is_cancelled_order(self):
        return self.status == settings.OSCAR_ORDER_STATUSES.CANCELLED

    def create_print_file(self, override=False):
        if self.print_file and not override:
            return False
        print_file_buffer = BytesIO()
        print_file_canvas = canvas.Canvas(
            print_file_buffer,
            pagesize=(PAGE_WIDTH_PT, PAGE_HEIGHT_PT),
            enforceColorSpace='sep_cmyk',
            initialFontName=FONT_NAME
        )
        facemasks_to_print = []
        total_facemasks = 0
        total_prints = 0
        current_print_number = 1

        # For all order lines, make sure the mask images are created
        for line in self.lines.all():
            try:
                mask_image_id = line.attributes.get(type='mask-image-id').value
            except LineAttribute.DoesNotExist:
                continue
            try:
                facemask = Facemask.objects.get(pk=mask_image_id)
            except Facemask.DoesNotExist:
                continue
            facemask.create_mask_image()
            facemasks_to_print.append({'facemask': facemask, 'line': line, 'quantity': line.quantity})
            total_facemasks += 1
            total_prints += line.quantity

        for print_info in facemasks_to_print:
            facemask = print_info['facemask']
            line = print_info['line']
            quantity = print_info['quantity']
            mask_image = ImageReader(facemask.mask_image.file)

            for q in range(quantity):
                # Image
                print_file_canvas.drawImage(
                    mask_image,
                    0, 0,
                    BLEED_WIDTH_PT, BLEED_HEIGHT_PT
                )
                if current_print_number == 1:
                    # Print shipping label
                    shipping_label_text = "Order #%s - %d masks<br/>%s" % (self.number, total_prints, self.shipping_address)
                    shipping_label = Paragraph(shipping_label_text, SHIPPING_LABEL_STYLE)
                    w, h = shipping_label.wrap(SHIPPING_LABEL_WIDTH, SHIPPING_LABEL_WIDTH)  # Height is not used
                    shipping_label.drawOn(print_file_canvas, SHIPPING_LABEL_OFFSET_X_PT, PAGE_HEIGHT_PT - SHIPPING_LABEL_OFFSET_Y_PT - h)
                # QR
                qr = self._get_qr('%s-%s-%s' % (self.number, line.id, q+1), QR_SIZE_PT)
                qr.rotate(QR_ROTATION)
                qr.drawOn(print_file_canvas, QR_OFFSET_X_PT, QR_OFFSET_Y_PT)
                # Cut lines
                CUTLINES_DRAWING.drawOn(print_file_canvas, CUTLINE_OFFSET_X_PT, CUTLINE_OFFSET_Y_PT)

                # Print more info in the corner
                print_file_canvas.setFont(FONT_NAME, ORDER_INFO_FONT_SIZE_PT)
                print_file_canvas.setFillColor(colors.black)
                print_file_canvas.drawString(ORDER_INFO_OFFSET_X_PT, ORDER_INFO_OFFSET_Y_PT, "Order #%s - Page %d/%d" % (self.number, current_print_number, total_prints))

                print_file_canvas.showPage()
                current_print_number += 1
        print_file_canvas.save()
        print_file_name = 'print_file_%s.pdf' % self.number
        self.print_file = SimpleUploadedFile(print_file_name, print_file_buffer.getvalue(), 'application/pdf')
        self.save()

    def _get_qr(self, qr_contents, qr_size) -> Drawing:
        qr_widget = QrCodeWidget(qr_contents)
        b = qr_widget.getBounds()

        w = b[2]-b[0]
        h = b[3]-b[1]

        qr_drawing = Drawing(qr_size, qr_size, transform=[float(qr_size)/w, 0, 0, float(qr_size)/h, 0, 0], initialFontName=FONT_NAME)
        qr_drawing.add(qr_widget)
        return qr_drawing


from oscar.apps.order.models import *  # noqa isort:skip

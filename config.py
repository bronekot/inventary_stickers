from reportlab.lib.units import mm

# Определяем размеры листа A4 в миллиметрах
A4_WIDTH_MM, A4_HEIGHT_MM = 210 * mm, 297 * mm
DPI = 96

# Определяем количество наклеек на одной строке и в одном столбце
NUM_LABELS_PER_ROW, NUM_LABELS_PER_COLUMN = 4, 10

# LABEL_PADDING = 10

LABEL_BORDER_MM = 5 * mm

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_size = 72

barcode_digits = 5
global_barcode_prefix = "PE"

# qr_size = int(min(label_width, label_height) * 2 / 3)
qr_border = 1

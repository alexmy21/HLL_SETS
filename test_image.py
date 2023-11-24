import random
import string
from PIL import Image
from io import BytesIO
from hll import Hll
from hll_set import HllSet

def image_to_bytes(image_path, size=1024):
    try:
        buffered = BytesIO()
        color_image = Image.open(image_path)
        #resize cplor_image to with + hight = size
        color_image.thumbnail((size, size))
        bw = color_image.convert('P', )
        bw.save(buffered, format="BMP")
        # print(bw.format, bw.size, bw.mode)
        return buffered.getvalue().hex()
    except Exception as e:
        print(f"Error converting {image_path}: {e}")
        return None

def image_to_hll(encoded_image, hll, ):
    for i in range(0, len(encoded_image)-1):
        hll.add(hex(i) + encoded_image[i])
    hll.card = round(hll.cardinality())
    return hll

hll_1 = Hll(13)
hll_1 = image_to_hll(image_to_bytes('data/DSCF6680.JPG', 512), hll_1, )

hll_2 = Hll(13)
hll_2 = image_to_hll(image_to_bytes('data/DSCF6681.JPG', 512), hll_2, )

hll_union = hll_1.union(hll_2)

u_set = HllSet(hll_union, label='U')
print('\nImage HllSet: ', u_set, u_set.card, u_set.delta, u_set.grad)


strings_1 = [''.join(random.choices(string.ascii_uppercase, k=10)) for _ in range(2000)]

u_set._append(strings_1)
print('\nImage and appended text HllSet: \n', u_set, u_set.card, u_set.delta, u_set.grad)

strings_2 = [''.join(random.choices(string.ascii_uppercase, k=10)) for _ in range(6000)]
u_set._append(strings_2)
print('\nImage and another appended text HllSet: \n', u_set, u_set.card, u_set.delta, u_set.grad)

strings_2 = [''.join(random.choices(string.ascii_uppercase, k=10)) for _ in range(6000)]
u_set.update(strings_2)
print('\nImage HllSet updated with text: \n', u_set, u_set.card, u_set.delta, u_set.grad)
from PIL import Image,ImageDraw,ImageFont
from settings import FONTS_PATH

def draw_captcha(text):
    image = Image.new('RGB', (300, 50), (220,210,190))
    draw = ImageDraw.Draw(image)

    # Create a text image
    textImg = Image.new('RGB',(150,40),(0,0,0))
    tmpDraw = ImageDraw.Draw(textImg)
    textFont = ImageFont.truetype(FONTS_PATH[0] + 'Arial.ttf',36)
    tmpDraw.text((0, 0), text, font = textFont, fill = (10,200,200))
    textImg = textImg.rotate(-10)

    # Create a mask (same size as the text image)
    mask = Image.new('L',(150, 40),0)
    mask.paste(textImg,(0,0))

    # Paste text image with the mask
    image.paste(textImg,(100,0),mask)
    return image

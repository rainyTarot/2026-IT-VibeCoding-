from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def radial_gradient(size, inner, outer, center=None, radius_scale=1.0):
    width, height = size
    cx, cy = center or (width // 2, height // 2)
    max_radius = ((width ** 2 + height ** 2) ** 0.5) / 2 * radius_scale
    image = Image.new("RGBA", size)
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy
            distance = min(((dx * dx + dy * dy) ** 0.5) / max_radius, 1.0)
            r = int(inner[0] + (outer[0] - inner[0]) * distance)
            g = int(inner[1] + (outer[1] - inner[1]) * distance)
            b = int(inner[2] + (outer[2] - inner[2]) * distance)
            a = int(inner[3] + (outer[3] - inner[3]) * distance)
            pixels[x, y] = (r, g, b, a)
    return image


def draw_starfield(draw, width, height, count):
    for index in range(count):
        x = (index * 97) % width
        y = (index * 57) % height
        radius = 1 + (index % 3)
        alpha = 80 + (index * 11) % 150
        draw.ellipse((x, y, x + radius, y + radius), fill=(190, 245, 255, alpha))


def make_background():
    size = (1280, 720)
    bg = radial_gradient(size, (8, 16, 38, 255), (2, 5, 16, 255), center=(640, 220), radius_scale=1.15)
    draw = ImageDraw.Draw(bg, "RGBA")
    draw_starfield(draw, *size, 140)

    draw.rounded_rectangle((140, 300, 1140, 700), radius=36, fill=(20, 36, 52, 240), outline=(80, 220, 255, 180), width=3)
    draw.rounded_rectangle((170, 325, 1110, 670), radius=28, fill=(24, 58, 46, 255), outline=(100, 255, 180, 120), width=2)

    for offset in range(0, 940, 85):
        x = 175 + offset
        draw.line((x, 330, x + 45, 667), fill=(110, 255, 220, 45), width=2)

    for y in (355, 470, 585):
        draw.rounded_rectangle((195, y, 1085, y + 18), radius=9, fill=(70, 160, 130, 80))

    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow, "RGBA")
    glow_draw.ellipse((260, 300, 1020, 760), fill=(60, 255, 200, 38))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    bg = Image.alpha_composite(bg, glow)

    bg.save(ASSETS / "bg_spaceship_farm.png")


def make_hole():
    size = (220, 140)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.ellipse((10, 40, 210, 120), fill=(10, 18, 22, 255), outline=(70, 240, 255, 160), width=4)
    draw.ellipse((28, 52, 192, 112), fill=(2, 4, 6, 255))
    draw.arc((8, 36, 212, 124), start=190, end=350, fill=(170, 255, 250, 180), width=3)
    draw.rounded_rectangle((34, 22, 186, 64), radius=18, fill=(58, 72, 90, 210), outline=(90, 220, 255, 120), width=2)
    img = img.filter(ImageFilter.GaussianBlur(0.3))
    img.save(ASSETS / "hole_neon.png")


def make_mole(hit=False):
    size = (220, 240)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    body = (60, 70, 160, 210)
    head = (45, 28, 175, 160)
    suit_color = (104, 90, 78, 255) if not hit else (160, 86, 90, 255)
    belly_color = (138, 124, 110, 255) if not hit else (210, 150, 150, 255)
    eye_color = (110, 250, 255, 255) if not hit else (255, 210, 90, 255)

    draw.ellipse(body, fill=suit_color)
    draw.ellipse(head, fill=suit_color)
    draw.ellipse((68, 92, 152, 178), fill=belly_color)
    draw.ellipse((25, 82, 75, 152), fill=suit_color)
    draw.ellipse((145, 82, 195, 152), fill=suit_color)
    draw.ellipse((78, 182, 110, 224), fill=suit_color)
    draw.ellipse((110, 182, 142, 224), fill=suit_color)

    draw.ellipse((74, 68, 104, 94), fill=eye_color)
    draw.ellipse((116, 68, 146, 94), fill=eye_color)
    draw.ellipse((84, 76, 94, 86), fill=(240, 255, 255, 255))
    draw.ellipse((126, 76, 136, 86), fill=(240, 255, 255, 255))
    draw.ellipse((88, 100, 132, 132), fill=(60, 40, 38, 255))
    draw.ellipse((95, 110, 107, 122), fill=(255, 180, 190, 255))
    draw.ellipse((113, 110, 125, 122), fill=(255, 180, 190, 255))

    if hit:
        draw.line((82, 68, 104, 92), fill=(255, 245, 170, 255), width=5)
        draw.line((82, 92, 104, 68), fill=(255, 245, 170, 255), width=5)
        draw.line((116, 68, 138, 92), fill=(255, 245, 170, 255), width=5)
        draw.line((116, 92, 138, 68), fill=(255, 245, 170, 255), width=5)
        draw.arc((82, 120, 138, 152), start=25, end=155, fill=(255, 240, 120, 255), width=5)
    else:
        draw.arc((84, 112, 136, 146), start=205, end=340, fill=(240, 225, 215, 255), width=4)

    visor = Image.new("RGBA", size, (0, 0, 0, 0))
    visor_draw = ImageDraw.Draw(visor, "RGBA")
    visor_draw.rounded_rectangle((58, 48, 162, 110), radius=26, fill=(40, 255, 255, 52), outline=(120, 255, 255, 180), width=3)
    visor = visor.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.alpha_composite(img, visor)

    if hit:
        spark = Image.new("RGBA", size, (0, 0, 0, 0))
        spark_draw = ImageDraw.Draw(spark, "RGBA")
        spark_draw.regular_polygon((110, 44, 22), n_sides=8, rotation=0, fill=(255, 210, 80, 210))
        spark = spark.filter(ImageFilter.GaussianBlur(1))
        img = Image.alpha_composite(img, spark)

    img.save(ASSETS / ("mole_hit.png" if hit else "mole_idle.png"))


def make_crosshair():
    size = (192, 192)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.ellipse((28, 28, 164, 164), outline=(120, 245, 255, 255), width=6)
    draw.ellipse((54, 54, 138, 138), outline=(120, 245, 255, 170), width=3)
    draw.line((96, 8, 96, 44), fill=(255, 80, 80, 255), width=5)
    draw.line((96, 148, 96, 184), fill=(255, 80, 80, 255), width=5)
    draw.line((8, 96, 44, 96), fill=(255, 80, 80, 255), width=5)
    draw.line((148, 96, 184, 96), fill=(255, 80, 80, 255), width=5)
    draw.ellipse((88, 88, 104, 104), fill=(255, 90, 100, 255))
    img = img.filter(ImageFilter.GaussianBlur(0.2))
    img.save(ASSETS / "crosshair_laser.png")


def make_panel():
    size = (520, 150)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((8, 8, 512, 142), radius=26, fill=(12, 26, 40, 220), outline=(70, 240, 255, 255), width=3)
    draw.rounded_rectangle((28, 28, 492, 122), radius=18, fill=(15, 44, 64, 180), outline=(120, 255, 220, 90), width=2)
    draw.rectangle((48, 46, 472, 54), fill=(255, 90, 90, 120))
    draw.rectangle((48, 96, 472, 104), fill=(80, 255, 190, 120))
    img = img.filter(ImageFilter.GaussianBlur(0.15))
    img.save(ASSETS / "ui_panel.png")


def make_button():
    size = (300, 96)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((6, 6, 294, 90), radius=24, fill=(18, 40, 62, 245), outline=(100, 245, 255, 255), width=3)
    draw.rounded_rectangle((22, 20, 278, 76), radius=18, fill=(34, 98, 110, 220))
    draw.rectangle((36, 24, 264, 38), fill=(170, 255, 250, 52))
    draw.polygon([(48, 48), (86, 48), (106, 32), (200, 32), (220, 48), (252, 48), (252, 62), (220, 62), (200, 78), (106, 78), (86, 62), (48, 62)], fill=(110, 255, 210, 110))
    img = img.filter(ImageFilter.GaussianBlur(0.15))
    img.save(ASSETS / "button_frame.png")


def make_preview_sheet():
    canvas = Image.new("RGBA", (1400, 1000), (5, 10, 24, 255))
    bg = Image.open(ASSETS / "bg_spaceship_farm.png").resize((1200, 675))
    canvas.paste(bg, (100, 50))

    hole = Image.open(ASSETS / "hole_neon.png")
    mole = Image.open(ASSETS / "mole_idle.png")
    hit = Image.open(ASSETS / "mole_hit.png")
    crosshair = Image.open(ASSETS / "crosshair_laser.png").resize((130, 130))
    panel = Image.open(ASSETS / "ui_panel.png").resize((420, 122))
    button = Image.open(ASSETS / "button_frame.png").resize((240, 76))

    preview_positions = [
        (300, 300), (600, 300), (900, 300),
        (300, 415), (600, 415), (900, 415),
        (300, 530), (600, 530), (900, 530),
    ]
    for x, y in preview_positions:
        canvas.paste(hole, (x, y), hole)

    idle_preview = mole.resize((145, 158))
    hit_preview = hit.resize((145, 158))
    canvas.paste(idle_preview, (554, 220), idle_preview)
    canvas.paste(hit_preview, (939, 415), hit_preview)
    canvas.paste(crosshair, (1040, 735), crosshair)
    canvas.paste(panel, (120, 700), panel)
    canvas.paste(button, (1080, 120), button)

    canvas.save(ASSETS / "asset_preview_sheet.png")


def main():
    make_background()
    make_hole()
    make_mole(hit=False)
    make_mole(hit=True)
    make_crosshair()
    make_panel()
    make_button()
    make_preview_sheet()


if __name__ == "__main__":
    main()

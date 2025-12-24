from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH, HEIGHT = 1920, 1080
PRIMARY = "#FFD54F"
WHITE = "#FFFFFF"
MUTED = (255, 255, 255, 200)

ZONES = {
    "genres": (420, 80),
    "title": (160, 190),
    "season": (160, 280),
    "rating": (160, 360),
    "studio_label": (640, 360),
    "studio": (640, 400),
    "synopsis": (160, 560, 900),
    "character": (1180, 60)
}

def wrap_text(draw, text, font, x, y, max_width, max_height=280):
    words = text.split()
    line = ""
    start_y = y
    for word in words:
        test = line + word + " "
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            draw.text((x, y), line, fill=MUTED, font=font)
            y += font.size + 8
            line = word + " "
        if y - start_y > max_height:
            draw.text((x, y), "...", fill=MUTED, font=font)
            return
    draw.text((x, y), line, fill=MUTED, font=font)

def draw_genres(draw, genres, font):
    x, y = ZONES["genres"]
    for g in genres.split(","):
        g = g.strip().upper()
        pad_x, pad_y = 20, 10
        w = draw.textlength(g, font=font)
        rect = (x, y, x + w + pad_x * 2, y + font.size + pad_y * 2)
        draw.rounded_rectangle(rect, 30, fill=WHITE)
        draw.text((x + pad_x, y + pad_y), g, fill="black", font=font)
        x = rect[2] + 16

def generate_poster(bg_path, data, character_path, output="final.png"):
    bg = Image.open(bg_path).convert("RGBA").resize((WIDTH, HEIGHT))
    bg = bg.filter(ImageFilter.GaussianBlur(2))

    template = Image.open("templates/1000042652-removebg-preview.png").convert("RGBA")
    template = template.resize((WIDTH, HEIGHT))

    canvas = Image.alpha_composite(bg, template)
    draw = ImageDraw.Draw(canvas)

    title_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 76)
    sub_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 46)
    body_font = ImageFont.truetype("fonts/Poppins-Regular.ttf", 28)
    pill_font = ImageFont.truetype("fonts/Poppins-Regular.ttf", 28)
    label_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 34)

    draw_genres(draw, data["genres"], pill_font)

    draw.text(ZONES["title"], data["title"].upper(), fill=PRIMARY, font=title_font)
    draw.text(ZONES["season"], data["season"].upper(), fill=WHITE, font=sub_font)

    draw.text(
        ZONES["rating"],
        f"RATING : {data['average_rating']}/10",
        fill=WHITE,
        font=body_font
    )

    draw.text(ZONES["studio_label"], "STUDIO", fill=WHITE, font=label_font)
    draw.text(ZONES["studio"], data["studio"].upper(), fill=PRIMARY, font=label_font)

    sx, sy, sw = ZONES["synopsis"]
    draw.text((sx, sy - 40), "SYNOPSIS :", fill=PRIMARY, font=label_font)
    wrap_text(draw, data["synopsis"], body_font, sx, sy, sw)

    char = Image.open(character_path).convert("RGBA").resize((650, 980))
    shadow = char.copy().filter(ImageFilter.GaussianBlur(14))
    canvas.paste(shadow, (ZONES["character"][0] - 10, ZONES["character"][1] + 10), shadow)
    canvas.paste(char, ZONES["character"], char)

    canvas.save(output)
    return output

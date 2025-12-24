from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH, HEIGHT = 1920, 1080

def draw_wrapped(draw, text, font, x, y, max_width):
    words = text.split()
    line = ""
    for word in words:
        test = line + word + " "
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            draw.text((x, y), line, fill="white", font=font)
            y += font.size + 8
            line = word + " "
    draw.text((x, y), line, fill="white", font=font)
    return y + font.size


def generate_poster(bg_path, data, output="final.png"):
    bg = Image.open(bg_path).convert("RGBA")
    bg = bg.resize((WIDTH, HEIGHT))

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 160))
    bg = Image.alpha_composite(bg, overlay)

    draw = ImageDraw.Draw(bg)

    title_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 72)
    label_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 36)
    body_font  = ImageFont.truetype("fonts/Poppins-Regular.ttf", 28)

    x = 80
    y = 100

    draw.text((x, y), data["title"].upper(), fill="#FFD54F", font=title_font)
    y += 90

    meta = [
        f"Genres: {data.get('genres','')}",
        f"Type: {data.get('type','')}",
        f"Rating: {data.get('average_rating','')}/100",
        f"Episodes: {data.get('no_of_episodes','')}",
        f"Status: {data.get('status','')}",
    ]

    for m in meta:
        draw.text((x, y), m, fill="white", font=body_font)
        y += 38

    y += 30
    draw.text((x, y), "SYNOPSIS :", fill="#FFD54F", font=label_font)
    y += 50

    synopsis = data.get("synopsis", "")
    draw_wrapped(draw, synopsis, body_font, x, y, 900)

    bg.save(output)
    return output

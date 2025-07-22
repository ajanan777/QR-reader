from PIL import Image, ImageColor

def matrix_to_image(matrix, scale=10, quiet_zone_modules=4, fg="#000000", bg="#ffffff"):
    """
    Renders the QR code matrix into a PIL Image with custom colours and scaling.

    Args:
        matrix (list of list of int): The QR code matrix (0 = white, 1 = black).
        scale (int): Pixel size of each module (default 10).
        quiet_zone_modules (int): Width of quiet zone (in modules).
        fg (str): Foreground colour (hex string, e.g., "#000000").
        bg (str): Background colour (hex string, e.g., "#ffffff").

    Returns:
        PIL.Image.Image: The rendered QR code image.
    """
    size = len(matrix)
    full_size = size + 2 * quiet_zone_modules

    # Convert hex to RGB
    fg_rgb = ImageColor.getrgb(fg)
    bg_rgb = ImageColor.getrgb(bg)

    # Create image with background colour
    img = Image.new("RGB", (full_size, full_size), bg_rgb)

    # Draw QR modules
    for r in range(size):
        for c in range(size):
            if matrix[r][c] == 1:
                x = c + quiet_zone_modules
                y = r + quiet_zone_modules
                img.putpixel((x, y), fg_rgb)

    # Scale up for visibility
    img = img.resize((full_size * scale, full_size * scale), Image.NEAREST)
    return img

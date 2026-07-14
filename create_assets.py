#!/usr/bin/env python
"""Create UI assets for the game."""
from PIL import Image, ImageDraw, ImageFont
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "images")
os.makedirs(ASSETS_DIR, exist_ok=True)

def create_wallpaper():
    """Create a nice airport-themed wallpaper."""
    img = Image.new('RGB', (1920, 1080), (15, 20, 35))
    draw = ImageDraw.Draw(img)
    
    # Gradient background
    for y in range(1080):
        r = int(15 + (25 - 15) * y / 1080)
        g = int(20 + (30 - 20) * y / 1080)
        b = int(35 + (50 - 35) * y / 1080)
        draw.line([(0, y), (1920, y)], fill=(r, g, b))
    
    # Runway lines
    for i in range(5):
        y = 200 + i * 180
        draw.rectangle([100, y, 1820, y + 60], fill=(40, 45, 55))
        # Center line
        draw.line([(500, y + 30), (1420, y + 30)], fill=(100, 100, 110), width=3)
        # Threshold marks
        for x in range(520, 1400, 80):
            draw.rectangle([x, y + 20, x + 30, y + 40], fill=(180, 180, 180))
    
    # Taxiways
    draw.line([(960, 0), (960, 1080)], fill=(50, 55, 65), width=40)
    draw.line([(0, 540), (1920, 540)], fill=(50, 55, 65), width=30)
    
    # Center marking
    draw.ellipse([920, 500, 1000, 580], outline=(100, 180, 220), width=3)
    draw.line([(960, 460), (960, 500)], fill=(100, 180, 220), width=3)
    draw.line([(960, 580), (960, 620)], fill=(100, 180, 220), width=3)
    draw.line([(920, 540), (960, 540)], fill=(100, 180, 220), width=3)
    draw.line([(1000, 540), (1040, 540)], fill=(100, 180, 220), width=3)
    
    # Terminal building silhouette
    draw.rectangle([150, 380, 400, 500], fill=(30, 35, 50))
    draw.rectangle([160, 360, 390, 380], fill=(35, 40, 55))
    # Windows
    for y in range(390, 490, 25):
        for x in range(170, 380, 40):
            draw.rectangle([x, y, x + 20, y + 15], fill=(60, 80, 120))
    
    # Control tower
    draw.rectangle([1700, 200, 1800, 600], fill=(30, 35, 50))
    draw.ellipse([1680, 150, 1820, 250], fill=(35, 40, 55))
    # Tower windows
    for y in range(160, 230, 20):
        draw.ellipse([1690, y, 1810, y + 15], fill=(100, 180, 220))
    for y in range(220, 580, 35):
        draw.rectangle([1710, y, 1790, y + 20], fill=(60, 80, 120))
    
    # Aircraft on ground (silhouettes)
    # Plane 1
    draw.polygon([(300, 700), (280, 720), (320, 720)], fill=(40, 45, 60))
    draw.polygon([(290, 710), (260, 730), (260, 740), (290, 720)], fill=(40, 45, 60))
    draw.polygon([(310, 710), (340, 730), (340, 740), (310, 720)], fill=(40, 45, 60))
    
    # Plane 2
    draw.polygon([(1600, 800), (1580, 820), (1620, 820)], fill=(40, 45, 60))
    draw.polygon([(1590, 810), (1560, 830), (1560, 840), (1590, 820)], fill=(40, 45, 60))
    draw.polygon([(1610, 810), (1640, 830), (1640, 840), (1610, 820)], fill=(40, 45, 60))
    
    # Grid lines on ground
    for x in range(0, 1920, 100):
        draw.line([(x, 0), (x, 1080)], fill=(25, 30, 45, 30), width=1)
    for y in range(0, 1080, 100):
        draw.line([(0, y), (1920, y)], fill=(25, 30, 45, 30), width=1)
    
    # Title text area (top)
    overlay = Image.new('RGBA', (1920, 180), (0, 0, 0, 180))
    img.paste(overlay, (0, 0), overlay)
    
    # Save
    img.save(os.path.join(ASSETS_DIR, "Wallpaper.png"), quality=95)
    print(f"Created Wallpaper.png")

def create_icons():
    """Create app icons in various sizes."""
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    
    for size in sizes:
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        w, h = size
        margin = w // 8
        
        # Background circle
        draw.ellipse([margin, margin, w-margin, h-margin], fill=(15, 30, 50, 255), outline=(100, 180, 220, 255), width=max(1, w//32))
        
        # Runway
        rw_w = w - margin * 2
        rw_h = h // 8
        rw_x = margin
        rw_y = h // 2 - rw_h // 2
        draw.rectangle([rw_x, rw_y, rw_x + rw_w, rw_y + rw_h], fill=(60, 65, 80, 255))
        # Center line
        draw.line([(rw_x + rw_w//4, rw_y + rw_h//2), (rw_x + 3*rw_w//4, rw_y + rw_h//2)], 
                  fill=(180, 180, 180, 255), width=max(1, w//64))
        # Threshold marks
        for i in range(3):
            x = rw_x + rw_w//4 + i * rw_w//4
            draw.rectangle([x, rw_y + rw_h//3, x + rw_w//20, rw_y + 2*rw_h//3], fill=(180, 180, 180, 255))
        
        # Tower
        tw_w = w // 5
        tw_h = h // 2
        tw_x = w // 2 - tw_w // 2
        tw_y = margin + h // 8
        draw.rectangle([tw_x, tw_y, tw_x + tw_w, tw_y + tw_h], fill=(35, 40, 60, 255))
        # Tower top
        draw.ellipse([tw_x - tw_w//4, tw_y - tw_h//6, tw_x + tw_w + tw_w//4, tw_y + tw_h//3], 
                     fill=(40, 45, 65, 255))
        # Windows
        for i in range(3):
            wy = tw_y + tw_h//4 + i * tw_h//3
            draw.rectangle([tw_x + tw_w//5, wy, tw_x + 4*tw_w//5, wy + tw_h//8], fill=(80, 140, 200, 255))
        
        # Aircraft
        ac_size = min(w, h) // 5
        ac_x = w - margin - ac_size
        ac_y = margin + h // 8
        # Body
        draw.polygon([(ac_x, ac_y + ac_size//2), 
                      (ac_x - ac_size//2, ac_y + ac_size), 
                      (ac_x + ac_size//2, ac_y + ac_size)], fill=(150, 200, 240, 255))
        # Wings
        draw.polygon([(ac_x - ac_size//3, ac_y + ac_size//2),
                      (ac_x - ac_size, ac_y + ac_size//2),
                      (ac_x - ac_size, ac_y + 2*ac_size//3),
                      (ac_x - ac_size//3, ac_y + 2*ac_size//3)], fill=(150, 200, 240, 255))
        draw.polygon([(ac_x + ac_size//3, ac_y + ac_size//2),
                      (ac_x + ac_size, ac_y + ac_size//2),
                      (ac_x + ac_size, ac_y + 2*ac_size//3),
                      (ac_x + ac_size//3, ac_y + 2*ac_size//3)], fill=(150, 200, 240, 255))
        
        # Save
        filename = f"icon_{size[0]}.png"
        img.save(os.path.join(ASSETS_DIR, filename))
        print(f"Created {filename}")
    
    # Create .ico from the 256x256
    ico_img = Image.open(os.path.join(ASSETS_DIR, "icon_256.png"))
    ico_img.save(os.path.join(ASSETS_DIR, "AirplaneGameICO.ico"), 
                 format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("Created AirplaneGameICO.ico")

def create_ui_icons():
    """Create small UI icons for buttons."""
    icons = {
        "buy": ("🛒", (0, 180, 220)),
        "repair": ("🔧", (255, 180, 50)),
        "advertise": ("📢", (180, 100, 220)),
        "refuel": ("⛽", (100, 220, 100)),
        "schedule": ("📅", (220, 150, 50)),
        "save": ("💾", (100, 220, 180)),
        "menu": ("🏠", (180, 180, 180)),
        "settings": ("⚙️", (150, 150, 150)),
    }
    
    for name, (symbol, color) in icons.items():
        for size in [32, 48, 64]:
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Circle background
            margin = 2
            draw.ellipse([margin, margin, size-margin, size-margin], 
                        fill=(30, 35, 50, 255), outline=color, width=2)
            
            # Try to draw emoji as text (will show as box if no font)
            try:
                font = ImageFont.truetype("seguiemj.ttf", size//2)
            except:
                font = ImageFont.load_default()
            
            # Draw symbol
            bbox = draw.textbbox((0, 0), symbol, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text((size//2 - tw//2, size//2 - th//2), symbol, font=font, fill=color)
            
            img.save(os.path.join(ASSETS_DIR, f"ui_{name}_{size}.png"))
        print(f"Created ui_{name}_*.png")

def create_aircraft_silhouettes():
    """Create simple aircraft silhouette images."""
    aircraft_types = {
        "C172": {"wingspan": 1.0, "length": 0.8, "color": (150, 200, 240)},
        "A320": {"wingspan": 1.2, "length": 1.0, "color": (180, 220, 180)},
        "B737": {"wingspan": 1.2, "length": 1.0, "color": (200, 220, 160)},
        "A380": {"wingspan": 1.5, "length": 1.3, "color": (220, 200, 160)},
    }
    
    for name, spec in aircraft_types.items():
        size = 128
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        cx, cy = size // 2, size // 2
        ws = int(size * 0.4 * spec["wingspan"])
        ln = int(size * 0.4 * spec["length"])
        color = spec["color"]
        
        # Fuselage
        draw.polygon([
            (cx, cy - ln//2),
            (cx - ln//8, cy + ln//2),
            (cx + ln//8, cy + ln//2),
        ], fill=color + (255,))
        
        # Wings
        draw.polygon([
            (cx - ws//2, cy - ln//6),
            (cx - ln//6, cy - ln//6),
            (cx - ln//6, cy + ln//4),
            (cx - ws//2, cy + ln//4),
        ], fill=color + (255,))
        
        draw.polygon([
            (cx + ws//2, cy - ln//6),
            (cx + ln//6, cy - ln//6),
            (cx + ln//6, cy + ln//4),
            (cx + ws//2, cy + ln//4),
        ], fill=color + (255,))
        
        # Tail
        draw.polygon([
            (cx, cy + ln//2),
            (cx - ln//8, cy + ln),
            (cx + ln//8, cy + ln),
        ], fill=color + (255,))
        
        # Cockpit
        draw.ellipse([cx - ln//10, cy - ln//2, cx + ln//10, cy - ln//3], 
                    fill=(180, 220, 255, 255))
        
        img.save(os.path.join(ASSETS_DIR, f"aircraft_{name}.png"))
        print(f"Created aircraft_{name}.png")

if __name__ == "__main__":
    print("Creating UI assets...")
    create_wallpaper()
    print()
    create_icons()
    print()
    create_ui_icons()
    print()
    create_aircraft_silhouettes()
    print("\nAll assets created!")
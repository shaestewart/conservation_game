import streamlit as st
from PIL import Image, ImageDraw
import random

# ------------------------------
# CONFIG
# ------------------------------
st.set_page_config(page_title="VHREC Virtual Forest 🌳", layout="wide")

# ------------------------------
# SESSION STATE
# ------------------------------
if "virtual_count" not in st.session_state:
    st.session_state.virtual_count = 0
if "real_count" not in st.session_state:
    st.session_state.real_count = 0
if "forest" not in st.session_state:
    st.session_state.forest = []

# ------------------------------
# FUNCTIONS
# ------------------------------
def plant_tree():
    """Add a new tree into forest list"""
    st.session_state.virtual_count += 1

    # Every 50 virtual trees = 1 real tree
    if st.session_state.virtual_count % 50 == 0:
        st.session_state.real_count += 1
        # 🔌 Hook 1ClickImpact API here with st.secrets["api_key"]

    # tree properties
    tree = {
        "x": random.randint(50, 950),
        "y": random.randint(300, 650),  # closer to bottom = closer to viewer
        "trunk_height": random.randint(20, 60),
        "trunk_width": random.randint(6, 12),
        "canopy_size": random.randint(30, 80),
        "shade": random.randint(100, 180)
    }
    st.session_state.forest.append(tree)


def draw_forest():
    """Render a forest from scratch with trees"""
    width, height = 1000, 700
    img = Image.new("RGB", (width, height), (120, 200, 120))  # background

    draw = ImageDraw.Draw(img)

    # simple gradient ground
    for y in range(height):
        shade = int(80 + (y / height) * 100)
        draw.line([(0, y), (width, y)], fill=(shade, 150 + y // 10, shade))

    # draw trees (back to front for depth)
    for tree in sorted(st.session_state.forest, key=lambda t: t["y"]):
        x, y = tree["x"], tree["y"]

        # trunk
        trunk_x0 = x - tree["trunk_width"] // 2
        trunk_y0 = y - tree["trunk_height"]
        trunk_x1 = x + tree["trunk_width"] // 2
        trunk_y1 = y
        draw.rectangle([trunk_x0, trunk_y0, trunk_x1, trunk_y1], fill=(90, 60, 30))

        # canopy (circle-ish blobs layered)
        for i in range(3):
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)
            r = tree["canopy_size"] - i * 10
            color = (0, tree["shade"] + i * 20, 0)
            draw.ellipse(
                [x - r + offset_x, trunk_y0 - r + offset_y,
                 x + r + offset_x, trunk_y0 + r + offset_y],
                fill=color, outline=None
            )

    return img


# ---------------

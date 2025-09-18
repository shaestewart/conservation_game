import streamlit as st
from PIL import Image, ImageDraw
import random
import os

# ------------------------------
# CONFIG
# ------------------------------
st.set_page_config(page_title="VHREC Virtual Forest 🌳", layout="wide")

# Load background (replace with your own forest bg)
BACKGROUND_PATH = "assets/forest_bg.png"
if os.path.exists(BACKGROUND_PATH):
    background = Image.open(BACKGROUND_PATH).convert("RGBA")
else:
    # fallback: green gradient background
    background = Image.new("RGBA", (1000, 700), (100, 180, 100, 255))
    draw = ImageDraw.Draw(background)
    for y in range(700):
        shade = 100 + int(80 * (y / 700))
        draw.line([(0, y), (1000, y)], fill=(shade, 180, shade, 255))

# Load tree assets
TREE_PATHS = [
    "assets/tree1.png",  # pine
    "assets/tree2.png",  # oak
    "assets/tree3.png",  # birch
]
tree_images = [Image.open(p).convert("RGBA") for p in TREE_PATHS if os.path.exists(p)]

if not tree_images:
    st.error("⚠️ No tree assets found in /assets. Add some PNGs with transparent backgrounds.")
    st.stop()

# ------------------------------
# SESSION STATE
# ------------------------------
if "forest" not in st.session_state:
    st.session_state.forest = []
if "virtual_count" not in st.session_state:
    st.session_state.virtual_count = 0
if "real_count" not in st.session_state:
    st.session_state.real_count = 0

# ------------------------------
# FUNCTIONS
# ------------------------------
def plant_tree():
    """Add a new tree to the forest."""
    img = random.choice(tree_images)
    scale = random.uniform(0.6, 1.4)
    new_tree = {
        "img": img,
        "x": random.randint(50, background.width - 150),
        "y": random.randint(int(background.height * 0.5), background.height - 200),
        "scale": scale
    }
    st.session_state.forest.append(new_tree)
    st.session_state.virtual_count += 1

    # Every 50 virtual = 1 real tree
    if st.session_state.virtual_count % 50 == 0:
        st.session_state.real_count += 1
        # 🔌 Here you’d call 1ClickImpact API with st.secrets["api_key"]


def render_forest():
    """Render the forest image with all planted trees."""
    canvas = background.copy()
    for tree in st.session_state.forest:
        t_img = tree["img"].resize(
            (int(tree["img"].width * tree["scale"]), int(tree["img"].height * tree["scale"]))
        )
        canvas.paste(t_img, (tree["x"], tree["y"]), t_img)
    return canvas

# ------------------------------
# UI
# ------------------------------
st.title("🌳 Virtual Forest")
st.write("Plant virtual trees and we’ll plant real ones! Every 50 virtual = 1 real tree.")

col1, col2 = st.columns([2,1])

with col1:
    if st.button("🌱 Plant a Tree"):
        plant_tree()

    forest_img = render_forest()
    st.image(forest_img, use_container_width=True)

with col2:
    st.metric("🌲 Virtual Trees", st.session_state.virtual_count)
    st.metric("🌍 Real Trees Committed", st.session_state.real_count)

    st.markdown("---")
    st.markdown("💚 Want to help even more?")
    st.link_button("Donate $1 to Plant a Tree", "https://your-donation-link-here")

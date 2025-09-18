import streamlit as st
import pandas as pd
import requests
from pathlib import Path
import random

# ---------- CONFIG ----------
st.set_page_config(page_title="VHREC Virtual Forest", layout="wide")

DATA_FILE = Path("tree_data.csv")
TREES_PER_REAL = 50  # 50 virtual trees = 1 real tree
API_URL = "https://api.1clickimpact.com/v1/trees"

# ---------- DATA STORAGE ----------
if not DATA_FILE.exists():
    pd.DataFrame({"virtual_trees": [0], "real_trees": [0]}).to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE).iloc[0].to_dict()

def save_data(virtual, real):
    pd.DataFrame({"virtual_trees": [virtual], "real_trees": [real]}).to_csv(DATA_FILE, index=False)

# ---------- API CALL ----------
def plant_real_tree(num):
    try:
        headers = {"Authorization": f"Bearer {st.secrets['1CLICKIMPACT_API_KEY']}"}
        payload = {"trees": num}
        r = requests.post(API_URL, headers=headers, json=payload)
        if r.status_code == 200:
            return True
        else:
            st.error(f"API Error: {r.status_code} - {r.text}")
            return False
    except Exception as e:
        st.error(f"API request failed: {e}")
        return False

# ---------- STATE ----------
data = load_data()
if "virtual_trees" not in st.session_state:
    st.session_state.virtual_trees = data["virtual_trees"]
    st.session_state.real_trees = data["real_trees"]

# ---------- UI ----------
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .big-counter {
        font-size: 2rem;
        font-weight: bold;
        color: #2E7D32;
    }
    .forest {
        background-image: url('https://images.unsplash.com/photo-1501785888041-af3ef285b470');
        background-size: cover;
        border-radius: 12px;
        min-height: 500px;
        position: relative;
        overflow: hidden;
    }
    .tree {
        position: absolute;
        opacity: 0.95;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 Virtual Forest")
st.markdown("Click the button to plant trees. Every **50 virtual trees = 1 real tree planted!**")

# ---------- BUTTON ----------
if st.button("🌳 Plant a Tree", use_container_width=True):
    st.session_state.virtual_trees += 1

    # Check if we should plant real tree(s)
    expected_real = st.session_state.virtual_trees // TREES_PER_REAL
    if expected_real > st.session_state.real_trees:
        to_plant = expected_real - st.session_state.real_trees
        success = plant_real_tree(to_plant)
        if success:
            st.session_state.real_trees = expected_real

    save_data(st.session_state.virtual_trees, st.session_state.real_trees)

# ---------- COUNTERS ----------
st.markdown(f"<div class='center big-counter'>🌳 Virtual Trees: {st.session_state.virtual_trees}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='center big-counter'>🌱 Real Trees Planted: {st.session_state.real_trees}</div>", unsafe_allow_html=True)

# ---------- FOREST VISUAL ----------
st.subheader("Your Virtual Forest")

tree_images = [
    "https://img.icons8.com/fluency/96/deciduous-tree.png",
    "https://img.icons8.com/fluency/96/tree.png",
    "https://img.icons8.com/fluency/96/coniferous-tree.png"
]

forest_html = '<div class="forest">'
for i in range(st.session_state.virtual_trees):
    tree_url = random.choice(tree_images)
    x = random.randint(0, 90)
    y = random.randint(0, 90)
    forest_html += f'<img src="{tree_url}" class="tree" style="left:{x}%; top:{y}%; width:50px;">'
forest_html += '</div>'

st.markdown(forest_html, unsafe_allow_html=True)

# ---------- DONATION SECTION ----------
st.subheader("💚 Support the Forest")
if st.button("Donate $5 (Mock)", use_container_width=True):
    # Replace with real Stripe checkout integration
    st.success("✅ Thank you for your donation! (mock transaction)")

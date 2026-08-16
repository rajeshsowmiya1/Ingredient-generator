import streamlit as st
import pandas as pd
from io import BytesIO

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ingredient Generator",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# COLOUR PALETTE
# ============================================================

DARK_BROWN = "#3B2114"
RICH_BROWN = "#5A321D"
MEDIUM_BROWN = "#7A4A2A"
GOLD = "#D4A017"
RICH_GOLD = "#B8860B"
CREAM = "#FFF8E7"
LIGHT_CREAM = "#F7EED8"
WHITE = "#FFFFFF"
TEXT_BROWN = "#2F1B10"

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {CREAM};
        color: {TEXT_BROWN};
    }}

    .main-header {{
        background: linear-gradient(
            135deg,
            {DARK_BROWN},
            {RICH_BROWN}
        );
        padding: 25px 30px;
        border-radius: 14px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(59, 33, 20, 0.20);
    }}

    .main-header h1 {{
        color: {GOLD};
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }}

    .main-header p {{
        color: {CREAM};
        margin-top: 6px;
        margin-bottom: 0;
        font-size: 1rem;
    }}

    .section-title {{
        color: {DARK_BROWN};
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 10px;
        border-bottom: 2px solid {GOLD};
        padding-bottom: 6px;
    }}

    [data-testid="stSidebar"] {{
        background-color: {DARK_BROWN};
    }}

    [data-testid="stSidebar"] * {{
        color: {CREAM};
    }}

    [data-testid="stSidebar"] h2 {{
        color: {GOLD};
    }}

    .stButton > button {{
        background-color: {MEDIUM_BROWN};
        color: {WHITE};
        border: 1px solid {GOLD};
        border-radius: 8px;
        font-weight: 600;
    }}

    .stButton > button:hover {{
        background-color: {RICH_GOLD};
        color: {WHITE};
        border-color: {GOLD};
    }}

    .stDownloadButton > button {{
        background-color: {GOLD};
        color: {DARK_BROWN};
        border: none;
        border-radius: 8px;
        font-weight: 700;
    }}

    .stDownloadButton > button:hover {{
        background-color: {RICH_GOLD};
        color: {WHITE};
    }}

    .info-box {{
        background-color: {LIGHT_CREAM};
        border-left: 5px solid {GOLD};
        padding: 15px;
        border-radius: 8px;
        color: {TEXT_BROWN};
        margin-bottom: 20px;
    }}

    .footer {{
        text-align: center;
        color: {MEDIUM_BROWN};
        font-size: 0.85rem;
        margin-top: 30px;
        padding: 15px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
    <div class="main-header">
        <h1>🍛 Ingredient Generator</h1>
        <p>
            Prepare recipe-wise ingredient requirements
            quickly and accurately.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# IMPORTANT:
# KEEP YOUR EXISTING GROCERIES AND VEGETABLES LISTS HERE
# ============================================================

# Your existing:
#
# GROCERIES = [...]
#
# VEGETABLES = [...]
#
# Keep the complete lists from your previous app here.

# ============================================================
# SESSION STATE
# ============================================================

if "extra_ingredients" not in st.session_state:
    st.session_state.extra_ingredients = []

if "requirement" not in st.session_state:
    st.session_state.requirement = None

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        f"""
        <h2 style="color:{GOLD};">
            ⚙️ Ingredient Settings
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Add an ingredient that is not currently "
        "available in the master template."
    )

    st.markdown("---")

    new_ingredient = st.text_input(
        "New Ingredient Name",
        placeholder="Enter ingredient"
    )

    new_category = st.selectbox(
        "Category",
        [
            "Grocery",
            "Vegetables"
        ]
    )

    if st.button(
        "➕ Add Ingredient",
        use_container_width=True
    ):

        ingredient = new_ingredient.strip()

        existing = (
            GROCERIES
            + VEGETABLES
            + [
                x["Ingredients"]
                for x in st.session_state.extra_ingredients
            ]
        )

        if ingredient == "":
            st.warning("Please enter an ingredient name.")

        elif ingredient in existing:
            st.warning("This ingredient already exists.")

        else:

            st.session_state.extra_ingredients.append(
                {
                    "Ingredients": ingredient,
                    "Category": new_category
                }
            )

            st.success(
                f"{ingredient} added temporarily."
            )

    st.markdown("---")

    st.markdown(
        f"""
        <div style="
            background-color:{RICH_BROWN};
            padding:15px;
            border-radius:8px;
            color:{CREAM};
        ">
        <b style="color:{GOLD};">
        Master List
        </b>
        <br><br>
        Grocery Items: {len(GROCERIES)}
        <br>
        Vegetable Items: {len(VEGETABLES)}
        <br>
        Added Items: {len(st.session_state.extra_ingredients)}
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# INFORMATION
# ============================================================

st.markdown(
    f"""
    <div class="info-box">

    <b>How to use:</b><br>
    1. Enter the recipe name.<br>
    2. Generate the ingredient requirement.<br>
    3. Use the search box to find ingredients quickly.<br>
    4. Enter quantity and purchase unit.<br>
    5. Category can be edited if required.<br>
    6. Download the completed requirement as Excel.

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# RECIPE
# ============================================================

st.markdown(
    '<div class="section-title">🍛 Recipe Details</div>',
    unsafe_allow_html=True
)

recipe_name = st.text_input(
    "Recipe Name",
    placeholder="Example: Vegetable Biryani"
)

# ============================================================
# GENERATE REQUIREMENT
# ============================================================

if st.button(
    "✨ Generate Ingredient Requirement",
    type="primary",
    use_container_width=True
):

    if recipe_name.strip() == "":
        st.warning("Please enter the recipe name.")

    else:

        master_data = []

        for item in GROCERIES:
            master_data.append(
                {
                    "Ingredients": item,
                    "Category": "Grocery"
                }
            )

        for item in VEGETABLES:
            master_data.append(
                {
                    "Ingredients": item,
                    "Category": "Vegetables"
                }
            )

        master_data.extend(
            st.session_state.extra_ingredients
        )

        master_df = pd.DataFrame(master_data)

        master_df = master_df.drop_duplicates(
            subset=["Ingredients"],
            keep="first"
        ).reset_index(drop=True)

        requirement = master_df.copy()

        requirement.insert(
            0,
            "Recipe",
            recipe_name.strip()
        )

        requirement["Quantity"] = None
        requirement["Purchase Unit"] = ""

        requirement = requirement[
            [
                "Recipe",
                "Ingredients",
                "Category",
                "Quantity",
                "Purchase Unit"
            ]
        ]

        st.session_state.requirement = requirement

# ============================================================
# INGREDIENT REQUIREMENT
# ============================================================

if st.session_state.requirement is not None:

    st.markdown(
        '<div class="section-title">'
        '📋 Ingredient Requirement'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # SEARCH OPTIONS
    # ========================================================

    col_search, col_quantity = st.columns([3, 1])

    with col_search:

        search_text = st.text_input(
            "🔎 Search Ingredients",
            placeholder=(
                "Type ingredient name in Tamil or English..."
            ),
            key="ingredient_search"
        )

    with col_quantity:

        show_completed = st.checkbox(
            "Show only entered quantities"
        )

    # ========================================================
    # CREATE FILTERED VIEW
    # ========================================================

    display_df = st.session_state.requirement.copy()

    # Search ingredient names
    if search_text.strip():

        search_value = search_text.strip().casefold()

        display_df = display_df[
            display_df["Ingredients"]
            .astype(str)
            .str.casefold()
            .str.contains(
                search_value,
                na=False,
                regex=False
            )
        ]

    # Show only completed ingredients
    if show_completed:

        display_df = display_df[
            display_df["Quantity"].notna()
            & (
                display_df["Quantity"].astype(str).str.strip()
                != ""
            )
        ]

    # ========================================================
    # SEARCH RESULT COUNT
    # ========================================================

    st.caption(
        f"Showing {len(display_df)} of "
        f"{len(st.session_state.requirement)} ingredients"
    )

    # ========================================================
    # DATA EDITOR
    # ========================================================

    edited_df = st.data_editor(
        display_df,

        use_container_width=True,

        hide_index=True,

        num_rows="fixed",

        column_config={

            "Recipe": st.column_config.TextColumn(
                "Recipe",
                required=True
            ),

            "Ingredients": st.column_config.TextColumn(
                "Ingredients",
                help="Pre-loaded from master template",
                disabled=True
            ),

            "Category": st.column_config.SelectboxColumn(
                "Category",
                options=[
                    "Grocery",
                    "Vegetables"
                ],
                help="Automatically populated but editable",
                required=True
            ),

            "Quantity": st.column_config.NumberColumn(
                "Quantity",
                help="Enter required quantity",
                min_value=0,
                step=0.001,
                format="%.3f"
            ),

            "Purchase Unit": st.column_config.SelectboxColumn(
                "Purchase Unit",
                options=[
                    "kg",
                    "g",
                    "litre",
                    "ml",
                    "piece",
                    "dozen"
                ],
                help="Select purchase unit"
            )
        },

        disabled=[
            "Ingredients"
        ]
    )

    # ========================================================
    # SAVE EDITS BACK TO MASTER REQUIREMENT
    # ========================================================

    if not edited_df.empty:

        for _, edited_row in edited_df.iterrows():

            ingredient_name = edited_row["Ingredients"]

            mask = (
                st.session_state.requirement["Ingredients"]
                == ingredient_name
            )

            st.session_state.requirement.loc[
                mask,
                "Recipe"
            ] = edited_row["Recipe"]

            st.session_state.requirement.loc[
                mask,
                "Category"
            ] = edited_row["Category"]

            st.session_state.requirement.loc[
                mask,
                "Quantity"
            ] = edited_row["Quantity"]

            st.session_state.requirement.loc[
                mask,
                "Purchase Unit"
            ] = edited_row["Purchase Unit"]

    # ========================================================
    # SUMMARY
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📊 Requirement Summary'
        '</div>',
        unsafe_allow_html=True
    )

    total_ingredients = len(
        st.session_state.requirement
    )

    completed = (
        st.session_state.requirement["Quantity"]
        .notna()
        .sum()
    )

    remaining = (
        total_ingredients - completed
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Ingredients",
            total_ingredients
        )

    with col2:
        st.metric(
            "Quantities Entered",
            completed
        )

    with col3:
        st.metric(
            "Remaining",
            remaining
        )

    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '⬇️ Download'
        '</div>',
        unsafe_allow_html=True
    )

    download_df = st.session_state.requirement.copy()

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        download_df.to_excel(
            writer,
            index=False,
            sheet_name="Ingredient Requirement"
        )

    output.seek(0)

    safe_recipe_name = (
        recipe_name.strip()
        if recipe_name.strip()
        else "Recipe"
    )

    filename = (
        f"{safe_recipe_name} "
        f"- Ingredient Requirement.xlsx"
    )

    st.download_button(
        label="⬇️ Download Ingredient Requirement",
        data=output,
        file_name=filename,
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
    )

    # ========================================================
    # CLEAR
    # ========================================================

    if st.button(
        "🗑️ Clear Current Requirement",
        use_container_width=True
    ):

        st.session_state.requirement = None

        st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div class="footer">
        <b style="color:{DARK_BROWN};">
            Ingredient Generator
        </b>
        <br>
        Temporary Food Book Application
    </div>
    """,
    unsafe_allow_html=True
)

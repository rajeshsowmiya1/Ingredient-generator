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

    input {{
        background-color: {WHITE} !important;
        color: {TEXT_BROWN} !important;
    }}

    [data-testid="stDataEditor"] {{
        background-color: {WHITE};
        border-radius: 10px;
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
# APPLICATION HEADER
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
# MASTER GROCERY LIST
# ============================================================

GROCERIES = [
    "மஞ்சள் தூள்",
    "மைதா மாவு",
    "கல் உப்பு",
    "கோதுமை மாவு",
    "டேபிள் சால்ட்",
    "கிழங்கு மாவு",
    "சீரகம்",
    "கடலை மாவு",
    "குருமிளகு",
    "அரிசி மாவு",
    "சிறிய கடுகு",
    "கான்பிளவர் மாவு",
    "கடலைப்பருப்பு",
    "R.B. சோடா உப்பு",
    "வெ. உளுந்தம்பருப்பு",
    "நயம் பட்டை",
    "நெ.1 துவரம் பருப்பு",
    "நயம் கிராம்பு",
    "பாசிபருப்பு",
    "நயம் சோம்பு",
    "வடபருப்பு (பட்டாணி)",
    "கசகசா",
    "பாசிபயிறு",
    "ஏலக்காய்",
    "வரமிளகாய்",
    "ஜாதிக்காய்",
    "LG பெருங்காயம்",
    "பொட்டுக்கடலை",
    "வெந்தயம்",
    "வறுத்த நிலக்கடலை",
    "மண்டை வெல்லம்",
    "பச்சை நிலக்கடலை",
    "நாட்டு மல்லி",
    "குருமிளகுப்பொடி",
    "பெருங்காய பவுடர்",
    "நரசுஸ் காபி",
    "மல்லிப்பொடி (சக்தி)",
    "சன்ரைஸ் காபி",
    "மிளகாய் பொடி (சக்தி)",
    "பெரிய அப்பளம்",
    "இட்லி பொடி (சக்தி)",
    "அப்பளப்பூ",
    "கரம் மசாலா",
    "மோர் மிளகாய்",
    "கோதுமை ரவை",
    "வெள்ளை சுண்டக்கடலை",
    "வெள்ளை ரவை",
    "பெருந்தரி சக்கரை (சீனி)",
    "சாப்பாட்டு கோதுமை ரவை",
    "சில்லி மசாலாப்பொடி",
    "சம்பா கோதுமை",
    "சபீனா கிளீனிங் பவுடர்",
    "ஸ்பெஷல் புளி",
    "மணதக்காளி வத்தல்",
    "சாப்பாட்டு அரிசி (வெ. பொன்னி)",
    "சுண்ட வத்தல்",
    "BT பச்சரிசி",
    "தேங்காய் எண்ணெய்",
    "பிரியாணி அரிசி (சீரகசம்பா)",
    "ரீபன்ட் ஆயில் (கணபதி)",
    "பிரியாணி அரிசி (பாசுமதி)",
    "நல்லெண்ணெய்",
    "இட்லி அரிசி (வெள்ளை காடை)",
    "விளக்கெண்ணெய்",
    "நைலான் ஜவ்வரிசி",
    "டால்டா",
    "மலைப்பூண்டு",
    "நெய்",
    "பாயாச அடை (பிரியா)",
    "வெண்ணெய்",
    "உருட்டு உளுந்து",
    "முழு முந்திரி",
    "வெள்ளை எள்ளு",
    "அரை முந்திரி",
    "காய்ந்த சுக்கு",
    "திராட்சை",
    "பிஸ்தா பருப்பு",
    "கை கிளவுஸ்",
    "சாரா பருப்பு",
    "குங்குமப் பூ",
    "லெமன் பவுடர்",
    "கஸ்தூரி மேத்தி",
    "சிவப்புக்கலர் பவுடர்",
    "ரசப்பொடி (சக்தி)",
    "ரோஸ் மில்க் பவுடர்",
    "அம்மோனியா பால் பவுடர்",
    "கிரேப் பவுடர்",
    "சர்க்கரை இல்லாத கோவா",
    "ரோஸ் எசன்ஸ்",
    "வெள்ளை சோயா",
    "பாதாம் எசன்ஸ்",
    "கெட்டி அவுல்",
    "கிரேப் எசன்ஸ்",
    "கம்பு குருனை",
    "பைனாப்பிள் எசன்ஸ்",
    "பஜ்ஜி மாவு",
    "குளோப்ஜாமூன் பவுடர் (MTR)",
    "சுக்குபொடி",
    "நந்தி மார்க் ஜிலேபி பருப்பு",
    "பன்னீர்",
    "பிஸ்கட் அமோனியா",
    "கலாகந்த்",
    "டைமண்ட் கல்கண்டு",
    "பேரிச்சை",
    "(KTR) பன்னீர்",
    "பல்பொடி",
    "பச்சைக்கற்பூரம்",
    "தேய்ப்பு மஞ்சி (இரும்பு)",
    "பாதாம் பருப்பு",
    "தீப்பெட்டி",
    "நியூஸ் பேப்பர்",
    "அரசன் சோப்",
    "ஆயில் பேப்பர்",
    "குங்குமம்",
    "சூடம்",
    "சந்தனம்",
    "வினிகர்",
    "திருநீறு",
    "லெமன் சால்ட்",
    "சர்விங் கேப்",
    "3 ரோஸஸ் டீ",
    "டிஷ்யூ பேப்பர்",
    "பாதாம் மாஸ் பவுடர்",
    "பேக்கிங் பவுடர்",
    "மில்க் மைட்",
    "டீ வடிக்கட்டி",
    "சிக்கன் மசாலா பொடி (சக்தி)",
    "Dustbin Cover",
    "மட்டன் மசாலா பொடி (சக்தி)",
    "சாம்பார் பொடி",
    "செர்ரிபழம்",
    "சில்லி சாஸ்",
    "தக்காளி சாஸ்",
    "சோயா சாஸ்",
    "தேன்",
    "தண்ணீர் டம்ளர்",
    "காபி டம்ளர்",
    "பாயாச கப்",
    "சேமியா",
    "பேப்பர் ரோல்"
]

# ============================================================
# MASTER VEGETABLE LIST
# ============================================================

VEGETABLES = [
    "எலுமிச்சம்பழம்",
    "சின்ன வெங்காயம்",
    "பல்லாரி",
    "பச்சை மிளகாய்",
    "நாட்டுத்தக்காளி",
    "சேனை கிழங்கு",
    "உருளைக்கிழங்கு",
    "குடைமிளகாய்",
    "சி. குடைமிளகாய்",
    "வெங்காயத்தூள்",
    "வெள்ளை ஓட்டுத்தேங்காய்",
    "பல் பூண்டு",
    "பேபிகார்ன் உரித்தது",
    "சிப்பி காளான்",
    "முட்டைக்கோஸ்",
    "பட்டன் குடைகாளான்",
    "கேரட்",
    "சைவ மீன்",
    "கறிபீன்ஸ்",
    "சைவ மட்டன்",
    "முருங்கை காய்",
    "பைனாப்பிள்",
    "சிறிய பிஞ்சு கத்திரிக்காய்",
    "பால் காலை",
    "பெரிய கத்திரிக்காய்",
    "பால் மாலை",
    "பச்சை பட்டாணி",
    "டிபன் இலை",
    "டபுள் பீன்ஸ்",
    "சாப்பாட்டு இலை",
    "ஊட்டி காளிபிளவர்",
    "டர்னர் கோஸ்",
    "ராக்கூடை",
    "நூல் கோஸ்",
    "தட்டக்கூடை",
    "புடலங்காய்",
    "ஈக்குசீமார்",
    "முற்றியவிதை பூசணிக்காய்",
    "காடாதுணி",
    "பீட்ரூட்",
    "ஈரலை துண்டு கலர்",
    "அவரைக்காய்",
    "கொத்தவரைக்காய்",
    "மாங்காய்",
    "வாழைக்காய்",
    "முறம்",
    "பாகற்காய்",
    "ஈரலை துண்டு வெள்ளை",
    "பழைய துணி",
    "ஜனதாவேஷ்டி",
    "சவுக்கு விறகு",
    "கிளை கோஸ்",
    "கேஸ் சிலிண்டர்",
    "கருணைக்கிழங்கு",
    "கேஸ் அடுப்பு",
    "பூசணிக்காய்",
    "மிக்ஸி",
    "அரசாணிக்காய்",
    "அடுப்புக்கரி",
    "வெண்டைக்காய்",
    "தண்ணீர் கேன்",
    "ஆப்பிள் தக்காளி",
    "வெற்றிலை, பாக்கு",
    "மாங்காய் இஞ்சி",
    "வாழைப்பழம்",
    "நார் இஞ்சி",
    "சீட்லெஸ் திராட்சை",
    "மல்லிதழை",
    "பாக்கு தட்டு",
    "புதினா",
    "ரவுண்டு இலை",
    "கறிவேப்பிலை"
]

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

    st.markdown(
        "Add an ingredient that is not currently available "
        "in the master template."
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

        if ingredient == "":

            st.warning(
                "Please enter an ingredient name."
            )

        else:

            existing = (
                GROCERIES
                + VEGETABLES
                + [
                    x["Ingredients"]
                    for x in st.session_state.extra_ingredients
                ]
            )

            if ingredient in existing:

                st.warning(
                    "This ingredient already exists."
                )

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
        Temporary Master List
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
# INFORMATION BOX
# ============================================================

st.markdown(
    f"""
    <div class="info-box">

    <b>How to use:</b><br>

    1. Enter the recipe name.<br>
    2. Generate the ingredient requirement.<br>
    3. Use the search box to quickly locate ingredients.<br>
    4. Enter quantities in Column D.<br>
    5. Select the purchase unit in Column E.<br>
    6. Modify Category in Column C if required.<br>
    7. Download Excel or copy the text for sharing.

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# RECIPE SECTION
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
# GENERATE BUTTON
# ============================================================

if st.button(
    "✨ Generate Ingredient Requirement",
    type="primary",
    use_container_width=True
):

    if recipe_name.strip() == "":

        st.warning(
            "Please enter the recipe name."
        )

    else:

        master_data = []

        # Grocery ingredients
        for item in GROCERIES:

            master_data.append(
                {
                    "Ingredients": item,
                    "Category": "Grocery"
                }
            )

        # Vegetable ingredients
        for item in VEGETABLES:

            master_data.append(
                {
                    "Ingredients": item,
                    "Category": "Vegetables"
                }
            )

        # Temporarily added ingredients
        master_data.extend(
            st.session_state.extra_ingredients
        )

        master_df = pd.DataFrame(
            master_data
        )

        # Remove duplicates
        master_df = master_df.drop_duplicates(
            subset=["Ingredients"],
            keep="first"
        ).reset_index(drop=True)

        # Create final table
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
# REQUIREMENT TABLE
# ============================================================

if st.session_state.requirement is not None:

    st.markdown(
        '<div class="section-title">'
        '📋 Ingredient Requirement'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Ingredients are pre-loaded from the master lists. "
        "Use the search box to quickly locate an ingredient."
    )

    # ========================================================
    # SEARCH
    # ========================================================

    search_text = st.text_input(
        "🔎 Search Ingredients",
        placeholder="Type ingredient name in Tamil or English...",
        key="ingredient_search"
    )

    # ========================================================
    # FILTER DISPLAY ONLY
    # ========================================================

    if search_text.strip():

        search_value = (
            search_text
            .strip()
            .casefold()
        )

        display_df = (
            st.session_state.requirement[
                st.session_state.requirement["Ingredients"]
                .astype(str)
                .str.casefold()
                .str.contains(
                    search_value,
                    na=False,
                    regex=False
                )
            ]
            .copy()
        )

    else:

        display_df = (
            st.session_state.requirement.copy()
        )

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
                help="Recipe name",
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
        ],

        key="ingredient_editor"
    )

    # ========================================================
    # SAVE EDITS BACK TO FULL REQUIREMENT
    # ========================================================

    if not edited_df.empty:

        for _, row in edited_df.iterrows():

            ingredient_name = row["Ingredients"]

            mask = (
                st.session_state.requirement[
                    "Ingredients"
                ]
                == ingredient_name
            )

            st.session_state.requirement.loc[
                mask,
                "Recipe"
            ] = row["Recipe"]

            st.session_state.requirement.loc[
                mask,
                "Category"
            ] = row["Category"]

            st.session_state.requirement.loc[
                mask,
                "Quantity"
            ] = row["Quantity"]

            st.session_state.requirement.loc[
                mask,
                "Purchase Unit"
            ] = row["Purchase Unit"]

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

    completed_mask = (
        st.session_state.requirement["Quantity"]
        .notna()
    )

    completed = completed_mask.sum()

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
    # OUTPUT SECTION
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '⬇️ Download / Share'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # ONLY ROWS WITH QUANTITY
    # ========================================================

    completed_df = (
        st.session_state.requirement[
            st.session_state.requirement["Quantity"]
            .notna()
        ]
        .copy()
    )

    # Remove completely blank quantity values
    completed_df = completed_df[
        completed_df["Quantity"]
        .astype(str)
        .str.strip()
        != ""
    ]

    if completed_df.empty:

        st.info(
            "Enter at least one quantity to enable "
            "Excel and Text sharing."
        )

    else:

        # ====================================================
        # EXCEL DOWNLOAD
        # ====================================================

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            completed_df.to_excel(
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

        excel_filename = (
            f"{safe_recipe_name} "
            f"- Ingredient Requirement.xlsx"
        )

        st.download_button(
            label="📥 Download Excel",
            data=output.getvalue(),
            file_name=excel_filename,
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True
        )

        # ====================================================
        # CREATE TEXT VERSION
        # ====================================================

        text_lines = []

        text_lines.append(
            f"🍛 {safe_recipe_name.upper()}"
        )

        text_lines.append("")
        text_lines.append(
            "INGREDIENT REQUIREMENT"
        )

        text_lines.append(
            "----------------------------"
        )

        # ====================================================
        # GROUP BY CATEGORY
        # ====================================================

        categories = [
            "Grocery",
            "Vegetables"
        ]

        for category in categories:

            category_df = completed_df[
                completed_df["Category"]
                == category
            ]

            if category_df.empty:
                continue

            text_lines.append("")
            text_lines.append(
                f"📌 {category.upper()}"
            )

            for _, row in category_df.iterrows():

                ingredient = str(
                    row["Ingredients"]
                ).strip()

                quantity = row["Quantity"]

                unit = str(
                    row["Purchase Unit"]
                ).strip()

                # --------------------------------------------
                # FORMAT QUANTITY
                # --------------------------------------------

                try:

                    quantity_float = float(
                        quantity
                    )

                    if quantity_float.is_integer():

                        quantity_text = str(
                            int(quantity_float)
                        )

                    else:

                        quantity_text = (
                            f"{quantity_float:.3f}"
                            .rstrip("0")
                            .rstrip(".")
                        )

                except:

                    quantity_text = str(
                        quantity
                    )

                # --------------------------------------------
                # CREATE TEXT LINE
                # --------------------------------------------

                if unit:

                    text_lines.append(
                        f"• {ingredient} - "
                        f"{quantity_text} {unit}"
                    )

                else:

                    text_lines.append(
                        f"• {ingredient} - "
                        f"{quantity_text}"
                    )

        text_output = "\n".join(
            text_lines
        )

        # ====================================================
        # TEXT TO COPY / SHARE
        # ====================================================

        st.markdown(
            "**📱 Text to Share**"
        )

        st.caption(
            "Click inside the box, press Ctrl+A, then Ctrl+C "
            "to copy and paste into WhatsApp, SMS, email, etc."
        )

        st.text_area(
            "Copy the text below:",
            value=text_output,
            height=350,
            key="share_text"
        )

        # ====================================================
        # DOWNLOAD TEXT FILE
        # ====================================================

        text_filename = (
            f"{safe_recipe_name} "
            f"- Ingredient Requirement.txt"
        )

        st.download_button(
            label="📄 Download Text File",
            data=text_output,
            file_name=text_filename,
            mime="text/plain",
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

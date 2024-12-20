import streamlit as st

# Function to inject custom CSS (optional for consistent styling)
def inject_custom_css():
    st.markdown(
        """
        <style>
        .main {
            background-color: #F5F5F5; /* Light grey background */
        }
        .bold-text {
            font-weight: bold;
        }
        .centered {
            text-align: center;
        }
        .red-band {
            background-color: #8B0000; 
            padding: 10px; 
            border-radius: 5px; 
            color: white; 
            font-size: 24px; 
            font-weight: bold; 
            text-align: left; 
            width: 100%;
        }
        .button-style {
            font-weight: bold;
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Set page configuration and image
st.set_page_config(page_title="Eco-Score Calculator", page_icon="🌱")

# Inject custom CSS
inject_custom_css()

# Add an image and a title at the top
st.image("https://cdn.unitycms.io/images/2lnv07LWaRb8rdPxOqTKwI.jpg?op=ocroped&val=1200,630,1000,1000,0,0&sum=0ZCX2CRVbos", use_container_width=True)  # Replace "your_image.png" with the path to your image

st.title("Eco-Score Calculator")

# Eco-score data structure
eco_data = {
    "Energy": {
        "Equipment": {
            "Source of electricity": {
                "Green electricity (on site electricity: estimate)": "A",
                "Green electricity (on site electricity: consumption known)": "A",
                "Electricity (on site electricity: estimate)": "B",
                "Electricity (on site electricity: consumption known)": "B",
                "Diesel generator (consumption known)": "D",
                "Diesel generator (consumption estimate)": "D",
                "Indirect emissions, measured externally": None,
            },
            "Power consumption": {
                "Unknown power consumption": None,
                "Low power consumption": "A",
                "Average power consumption": "C",
                "High power consumption": "D",
            },
            "Power supply lighting": {
                "Including set lighting": "D",
                "Excluding set lighting": "B",
            },
        },
        "Location": {
            "Source": {
            "Locations: Green electricity (consumption known)": "A",
            "Locations: Electricity (consumption known)": "B",
            "Locations: Green electricity (generic)": "A",
            "Locations: Electricity demand (generic)": "B",
            "Indirect emissions, measured externally": None,
            }
        },
        "Film Studio": {
            "Source": {
                "Green electricity film studio (estimate)": "A",
                "Green electricity film studio (consumption known)": "A",
                "Electricity film studio (estimate)": "B",
                "Electricity film studio (consumption known)": "B",
                "Natural gas": "D",
                "Heating oil light": "D",
                "Liquefied petroleum gas": "D",
                "Indirect emissions, measured externally": None,
            },
            "Power consumption": {
                "Unknown power consumption": None,
                "Low power consumption": "A",
                "Average power consumption": "C",
                "High power consumption": "D",
            },
        },
        "Post-production (Film editing)": {
            "Source": {
                "Grading workstation": "B",
                "Grading workstation (green electricity)": "A",
                "Motion design workstation": "B",
                "Motion design workstation (green electricity)": "A",
                "Cutting/Editing workstation": "B",
                "Cutting/Editing workstation (green electricity)": "A",
                "Indirect emissions, measured externally": None,
            },
        },
        "Post-production (Sound editing)": {
            "Source": {
                "Sound design workstation": "B",
                "Sound design workstation (green electricity)": "A",
                "Indirect emissions, measured externally": None,
            },
        },
        "Post-production (Other)": {
            "Source": {
                "Hard disk archive": "C",
                "Cloud-Storage": "B",
                "Generic postproduction workstation": "C",
                "Generic postproduction workstation (green electricity)": "A",
                "Indirect emissions, measured externally": None,
            },
        },
        "Offices": {
            "Source": {
                "Offices: Heat demand (generic)": "D",
                "Offices: Electricity demand (generic)": "B",
                "Offices: Green electricity (generic)": "A",
                "Indirect emissions, measured externally": None,
            },
            "Fuel type": {
                "Unknown": None,
                "Natural gas": "D",
                "Liquid gas": "D",
                "Heating oil": "D",
                "Lignite": "D",
                "Cooking coal": "D",
                "Wood general": "B",
                "Wood pellets": "B",
                "Wood chips": "B",
                "District heat (average mix)": "C",
                "Electricity (average mix, CH)": "B",
                "Green electricity": "A",
            },
            "Building type": {
                "Office building, heated only": "B",
                "Office building, heated and air-conditioning": "C",
            },
            "Heat consumption": {
                "Average heat consumption": "C",
                "Low heat consumption": "A",
                "High heat consumption": "D",
            },
        },
    },
    "Travel/Transport": {
        "Accommodation": {
            "Source": {
                "Youth Hostel, shared room": "A",
                "Hotel (average, Switzerland)": "B",
                "Hotel (average, international)": "C",
                "Hotel (certified, climate-friendly, Switzerland)": "A",
                "Hotel (luxury class, Switzerland)": "D",
                "Indirect emissions, measured externally": None,
            },
        },
        "Passenger transport": {
            "Source": {
                "Diesel": "D",
                "Diesel by distance": "D",
                "Petrol": "D",
                "Petrol by distance": "D",
                "Electricity consumption": "B",
                "Electricity by distance": "B",
                "Green electricity consumption": "A",
                "Green electricity by distance": "A",
                "Car (distance estimate)": "D",
                "Public transport mix (Switzerland)": "A",
                "Autobus (Switzerland)": "B",
                "Cable car (Switzerland)": "B",
                "Coach": "C",
                "Long distance rail (Switzerland)": "A",
                "Long distance rail (Europe)": "A",
                "Passenger ship (Switzerland)": "B",
                "Indirect emissions, measured externally": None,
            },
            "Average fuel consumption": {
                "Between 2-5 L/100km": "A",
                "Between 5-7 L/100km": "B",
                "Between 7-10 L/100km": "C",
                "More than 10 L/100km": "D",
            },
        },
        "Logistics": {
            "Source": {
                "Diesel consumption": "D",
                "Petrol consumption": "D",
                "Natural gas (CNG) consumption": "D",
                "Biomethane (Bio-CNG) Consumption": "B",
                "Electricity consumption": "B",
                "Green electricity consumption": "A",
                "Logistics (road) external provider, generic": None,
                "Logistics (road) own, Ø consumption known": None,
                "Van 3.5t": "C",
                "Truck 7.5t": "C",
                "Truck 18t": "C",
                "Truck 26t": "C",
                "Truck 32t": "D",
                "Truck 40t": "D",
                "Transporter 3.5t (battery electric)": "A",
                "Lorry 7.5t (battery electric)": "A",
                "Lorry 18t (battery electric)": "A",
                "Lorry 26t (battery electric)": "A",
                "Articulated lorry 32t (battery electric)": "B",
                "Articulated lorry 40t (battery electric)": "B",
                "Train (average)": "A",
                "Container vessel (average)": "C",
                "Externally determined indirect emissions": None,
            },

        },
    },
    "Catering": {
        "Meals": {
            "Meat consumption": {
                "Mixed food diet": "C",
                "Meat-reduced": "B",
                "Vegetarian": "A",
                "Vegan": "A",
            },
            "Method of production": {
                "Conventional": "C",
                "Partially organic (ca. 50%)": "B",
                "Organic": "A",
            },
            "Regional, seasonal (specification of food)": {
                "Standard": "C",
                "Partially regional and seasonal": "B",
                "Regional and seasonal": "A",
            },
        },
        "Dishes": {
            "Source": {
                "Reusable cups": "A",
                "Disposable cups": "D",
                "Plates": "D",
                "Disposable cutlery": "D",
                "Indirect emissions, measured externally": None,
            },
        },
    },
    "Material": {
        "Set construction": {
            "Source": {
                "Flooring: linoleum floor": "B",
                "Flooring: solid wood parquet": "B",
                "Flooring: PVC": "D",
                "Flooring: PVC vinyl tile floor": "D",
                "Flooring: carpet": "C",
                "Wood construction: Beam/four-by-two/timber/slats": "B",
                "Wood construction: plywood": "B",
                "Wood construction: medium density fibreboard (MDF)": "D",
                "Timber construction (monetary estimate)": "B",
                "EPS hard foam for scenery construction (Styropor®)": "D",
                "Plasterboard: monetary estimation": "C",
                "Dispersion wall paint (m2)": "C",
                "Solvent-based varnish (m2)": "D",
                "Water-based paint (m2)": "C",
                "Other materials: foil roll": "D",
                "Other materials: gaffer tape": "D",
                "Indirect emissions, measured externally": None,
            },
        },
        "Prop vehicles": {
            "Source": {
                "Petrol": "D",
                "Diesel": "D",
                "Maritime Diesel Oil (MDO)": "D",
                "Indirect emissions, measured externally": None,
            },
        },
        "Costumes": {
            "Source": {
                "Costume rental/reuse": "A",
                "Costume purchase": "C",
                "Indirect emissions, measured externally": None,
            },
            "Laundry drying": {
                    "Tumble dryer": "D",
                    "Clothesline": "A",
            },
            "Laundry detergent": {
                    "Conventional": "D",
                    "Organic": "A",
            },
        },
        "Waste": {
            "Source": {
                "Residual waste (for incineration, kg)": "D",
                "Residual waste (for incineration, bags)": "D",
                "Indirect emissions, measured externally": None,
            },
        },
    },
}

# Map letter scores to numeric values
score_map = {"A": 1, "B": 2, "C": 3, "D": 4}

# Function to get color based on score (letter grades)
def get_score_color(letter_score):
    # Define colors for valid letter scores
    score_colors = {
        "A": "#4CAF50",         # Green
        "A-": "#8BC34A",        # Light Green
        "B+": "#FFEB3B",        # Light Yellow
        "B": "#FFC107",         # Yellow
        "B-": "#FFB300",        # Dark Yellow
        "C+": "#FF9800",        # Light Orange
        "C": "#FF5720",         # Orange
        "C-": "#E64A19",        # Darker Orange
        "D+": "#D84315",        # Red-Orange
        "D": "#B71C1C",         # Dark Red
    }

    # Handle invalid or missing scores
    if not letter_score or letter_score == "None" or letter_score == "No score":
        return "#9E9E9E"  # Gray for invalid or missing scores
    
    # Get the corresponding color or default to gray
    return score_colors.get(letter_score.upper(), "#9E9E9E")  # Default to gray

# Function to convert numeric score to letter score
def numeric_to_letter(score):
    if score == 1:
        return "A"
    elif 1 < score <= 1.5:
        return "A-"
    elif 1.5 < score < 2:
        return "B+"
    elif score == 2:
        return "B"
    elif 2 < score <= 2.5:
        return "B-"
    elif 2.5 < score < 3:
        return "C+"
    elif score == 3:
        return "C"
    elif 3 < score <= 3.5:
        return "C-"
    elif 3.5 < score < 4:
        return "D+"
    elif score == 4:
        return "D"
    else:
        return "N/A"


selected_options = {}  # Empty dictionary to store user selections

# Compute scores
def compute_scores(selected_options, category_percentages=None):
    """
    Computes scores for groups, subcategories, categories, and the overall score.

    Parameters:
        selected_options (dict): User-selected options structured as {category: {subcategory: {group: [options]}}}.
        category_percentages (dict): Percentages for categories (hidden from user). Must sum to 100.

    Returns:
        dict: Scores for groups, subcategories, categories, and the overall score.
    """
    scores = {
        "groups": {},        # Scores for each group
        "subcategories": {}, # Scores for each subcategory
        "categories": {},    # Scores for each category
        "overall_score": None  # Overall score
    }

    # Step 1: Calculate scores for groups
    for category, subcategories in selected_options.items():
        scores["groups"][category] = {}
        for subcategory, groups in subcategories.items():
            scores["groups"][category][subcategory] = {}
            for group, data in groups.items():
                # Filter out "No score" and None values for calculations
                valid_scores = [score_map[score] for score in data["scores"] if score not in ("No score", None)]

                if valid_scores:  # Only calculate if there are valid scores
                    group_avg_score = sum(valid_scores) / len(valid_scores)
                    scores["groups"][category][subcategory][group] = group_avg_score
                else:
                    scores["groups"][category][subcategory][group] = None

    # Step 2: Calculate scores for subcategories
    for category, subcategories in scores["groups"].items():
        scores["subcategories"][category] = {}
        for subcategory, groups in subcategories.items():
            valid_group_scores = [
                score for score in groups.values() if score is not None
            ]
            if valid_group_scores:
                subcategory_avg_score = sum(valid_group_scores) / len(valid_group_scores)
                scores["subcategories"][category][subcategory] = subcategory_avg_score
            else:
                scores["subcategories"][category][subcategory] = None # No valid group scores

    # Step 3: Calculate scores for categories
    for category, subcategories in scores["subcategories"].items():
        valid_subcategory_scores = [
            score for score in subcategories.values() if score is not None
        ]
        if valid_subcategory_scores:
            category_avg_score = sum(valid_subcategory_scores) / len(valid_subcategory_scores)
            scores["categories"][category] = category_avg_score
        else:
            scores["categories"][category] = None  # No valid subcategory scores

    # Step 4: Calculate overall score with percentages
    category_scores = [
        score
        for score in scores["categories"].values()
        if score is not None
    ]
    if category_scores:
        scores["overall_score"] = sum(category_scores) / len(category_scores)
    else:
        scores["overall_score"] = None  # No valid category scores

    return scores

# Display the options
# Step 1: Add a text input for the production title
production_title = st.text_input("Enter the title of the production", placeholder="e.g., Hockey game Servette vs LHC")

# Display the entered title dynamically (optional)
if production_title:
    st.markdown(f"### Computing Eco-Score for: **{production_title}**")

# Step 2: Dynamically display options for each category
for category, subcategories in eco_data.items():

    st.markdown(f"<div class='red-band'>{category}</div>", unsafe_allow_html=True)
    
    selected_options[category] = {} # Initialize category in selected options

    for subcategory, groups in subcategories.items():
        st.subheader(subcategory)
        selected_options[category][subcategory] = {} # Initialize subcategory

        for group, options in groups.items():
            st.markdown(f"<div class='bold-text'>{group}</div>", unsafe_allow_html=True)
            
            # Use st.multiselect to allow selecting multiple options
            selected_options_group = st.multiselect(
                f"Select options for {group}",
                options=list(options.keys()), # Available options
                key=f"{category}_{subcategory}_{group}", # Unique key for each group
            )

            # Store the selected options and their corresponding scores
            selected_options[category][subcategory][group] = {
                "options": selected_options_group,  # List of selected options
                "scores": [options[opt] if options[opt] is not None else "No score" for opt in selected_options_group],  # Corresponding scores
            }


# Function to calculate and display results
if st.button("Calculate Eco-Score"):
    # Perform the computations
    scores = compute_scores(selected_options)

    # Display overall eco-score
    overall_numeric_score = scores["overall_score"]
    overall_letter_score = numeric_to_letter(overall_numeric_score) if overall_numeric_score is not None else "No score"

    # Precompute overall numeric display
    overall_numeric_display = f"{overall_numeric_score:.2f}" if overall_numeric_score is not None else "N/A"

    st.markdown("<hr>", unsafe_allow_html=True)  # Separator

    # Overall Eco-Score
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; gap: 10px; padding: 20px;">
            <div style="flex: 1; background-color: #E0E0E0; color: black; padding: 20px; border-radius: 5px; font-size: 24px; font-weight: bold; text-align: center;">
                Overall Eco-Score
            </div>
            <div style="flex: 1; background-color: {get_score_color(overall_letter_score)}; color: white; padding: 20px; border-radius: 5px; font-size: 24px; font-weight: bold; text-align: center;">
                {overall_letter_score}
            </div>
            <div style="flex: 1; background-color: #E0E0E0; color: black; padding: 20px; border-radius: 5px; font-size: 24px; font-weight: bold; text-align: center;">
                {overall_numeric_display}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Display category scores
    st.markdown("<hr>", unsafe_allow_html=True)  # Separator
    for category, category_score in scores["categories"].items():
        category_letter_score = numeric_to_letter(category_score) if category_score is not None else "No score"

        # Precompute category numeric display
        category_numeric_display = f"{category_score:.2f}" if category_score is not None else "N/A"

        # Category Scores in a Colored Band
        st.markdown(
            f"""
            <div style="background-color: {get_score_color(category_letter_score)}; padding: 15px; border-radius: 5px; margin-bottom: 15px; color: white; font-size: 24px; font-weight: bold; display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1; text-align: left;">
                    {category}
                </div>
                <div style="flex: 1; text-align: center;">
                    {category_letter_score}
                </div>
                <div style="flex: 1; text-align: right;">
                    {category_numeric_display}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        
        # Expandable Subcategories for Each Category
        with st.expander(f"Show details for {category}"):
            for subcategory, subcategory_score in scores["subcategories"][category].items():
                # Check if the subcategory has options selected
                has_selected_options = any(
                    group_data["options"]
                    for group_data in selected_options[category][subcategory].values()
                )

                if not has_selected_options:
                    continue  # Skip subcategory if no options are selected

                subcategory_letter_score = numeric_to_letter(subcategory_score) if subcategory_score is not None else "No score"

                # Subcategory Name and Score on the Same Line
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: flex-start; align-items: center; margin: 10px 0;">
                        <span style="font-size: 20px; font-weight: bold; color: #8B0000; margin-right: 10px;">{subcategory}</span>
                        <span style="background-color: {get_score_color(subcategory_letter_score)}; color: white; padding: 5px 10px; border-radius: 5px; font-size: 20px; font-weight: bold; text-align: center;">
                            {subcategory_letter_score}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Display Groups and Their Selected Options
                for group, group_data in selected_options[category][subcategory].items():
                    if group_data["options"]:  # Only show groups with selected options
                        st.markdown(f"**{group}**")

                        # Display each selected option with its score
                        for option, score in zip(group_data["options"], group_data["scores"]):
                            score_color = get_score_color(score if score != "No score" else "No score")
                            st.markdown(
                                f"""
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-left: 20px; margin-bottom: 10px;">
                                    <span style="font-size: 16px;">{option}</span>
                                    <span style="background-color: {score_color}; color: white; padding: 15px 20px; border-radius: 5px; font-size: 16px; font-weight: bold; text-align: center; width: 75px; height: 40px; display: flex; justify-content: center; align-items: center;">
                                        {score}
                                    </span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )


# Correspondence of Scores
st.markdown("<hr>", unsafe_allow_html=True)  # Separator
st.markdown("<h3 style='text-align: center;'>Correspondence of Scores</h3>", unsafe_allow_html=True)

# Define the letter grades and their corresponding colors
score_colors = {
    "A": "#4CAF50",         # Green
    "A-": "#8BC34A",        # Light Green
    "B+": "#FFEB3B",        # Light Yellow
    "B": "#FFC107",         # Yellow
    "B-": "#FFB300",        # Dark Yellow
    "C+": "#FF9800",        # Light Orange
    "C": "#FF5720",         # Orange
    "C-": "#E64A19",        # Darker Orange
    "D+": "#D84315",        # Red-Orange
    "D": "#B71C1C",         # Dark Red
}

# Define the mapping for numbers under specific grades
number_mapping = {"A": 1, "B": 2, "C": 3, "D": 4}

# Create columns for each grade
columns = st.columns(len(score_colors))

# Add each grade box into its corresponding column
for i, (letter, color) in enumerate(score_colors.items()):
    with columns[i]:
        # Add the letter grade box
        st.markdown(
            f"""
            <div style="width: 50px; height: 50px; background-color: {color}; color: white; 
                        padding: 10px; border-radius: 5px; font-size: 20px; font-weight: bold; 
                        display: flex; justify-content: center; align-items: center; text-align: center;">
                {letter}
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Add the number below if the letter is in the mapping
        if letter in number_mapping:
            st.markdown(
                f"""
                <div style="width: 50px; height: 50px; background-color: #e0e0e0; color: black; 
                            padding: 10px; border-radius: 5px; font-size: 20px; font-weight: bold; 
                            display: flex; justify-content: center; align-items: center; text-align: center; margin-top: 5px;">
                    {number_mapping[letter]}
                </div>
                """,
                unsafe_allow_html=True,
            )


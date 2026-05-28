import streamlit as st
import pandas as pd
import os

# -----------------------------
# Setup
# -----------------------------

st.set_page_config(
    page_title="Campus Lost & Found",
    page_icon="🎒",
    layout="wide"
)

DATA_FILE = "lost_found_data.csv"
IMAGE_FOLDER = "images"

# Create image folder
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Create CSV if not exists
if not os.path.exists(DATA_FILE):

    df = pd.DataFrame(columns=[
        "Type",
        "Item Name",
        "Description",
        "Location",
        "Date",
        "Contact",
        "Image",
        "Collected"
    ])

    df.to_csv(DATA_FILE, index=False)

# Load data
df = pd.read_csv(DATA_FILE)

# -----------------------------
# Title
# -----------------------------

st.title("🎒 Campus Lost & Found System")

menu = st.sidebar.selectbox(
    "Choose Page",
    ["Upload Found Item", "Upload Lost Item", "Browse Items"]
)

# =========================================================
# Upload Found Item
# =========================================================

if menu == "Upload Found Item":

    st.header("Upload Found Item")

    with st.form("found_form"):

        item_name = st.text_input("Item Name")
        description = st.text_area("Description")
        location = st.text_input("Where was it found?")
        date = st.date_input("Date Found")
        contact = st.text_input("Your Contact Info")

        image = st.file_uploader(
            "Upload Image (Required)",
            type=["png", "jpg", "jpeg"]
        )

        submit = st.form_submit_button("Submit")

        if submit:

            if image is None:
                st.error("Image is required for found items!")

            else:
                image_name = image.name
                image_path = os.path.join(IMAGE_FOLDER, image_name)

                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())

                new_data = pd.DataFrame([{
                    "Type": "Found",
                    "Item Name": item_name,
                    "Description": description,
                    "Location": location,
                    "Date": date,
                    "Contact": contact,
                    "Image": image_name,
                    "Collected": False
                }])

                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)

                st.success("Found item uploaded successfully!")

# =========================================================
# Upload Lost Item
# =========================================================

elif menu == "Upload Lost Item":

    st.header("Upload Lost Item Request")

    with st.form("lost_form"):

        item_name = st.text_input("Lost Item Name")
        description = st.text_area("Describe the item")
        location = st.text_input("Where did you lose it?")
        date = st.date_input("Date Lost")
        contact = st.text_input("Your Contact Info")

        image = st.file_uploader(
            "Upload Image (Optional)",
            type=["png", "jpg", "jpeg"]
        )

        submit = st.form_submit_button("Submit")

        if submit:

            image_name = "No image uploaded"

            if image is not None:
                image_name = image.name
                image_path = os.path.join(IMAGE_FOLDER, image_name)

                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())

            new_data = pd.DataFrame([{
                "Type": "Lost",
                "Item Name": item_name,
                "Description": description,
                "Location": location,
                "Date": date,
                "Contact": contact,
                "Image": image_name,
                "Collected": False
            }])

            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            st.success("Lost item request uploaded!")

# =========================================================
# Browse Items
# =========================================================

elif menu == "Browse Items":

    st.header("Browse Items")

    # Filter
    filter_type = st.selectbox(
        "Filter by Type",
        ["All", "Found", "Lost"]
    )

    if filter_type != "All":
        filtered_df = df[df["Type"] == filter_type]
    else:
        filtered_df = df

    # Split data
    active_items = filtered_df[filtered_df["Collected"] == False]
    claimed_items = filtered_df[filtered_df["Collected"] == True]

    # -----------------------------
    # ACTIVE ITEMS
    # -----------------------------

    st.subheader("🔍 Still In Search")

    if active_items.empty:
        st.info("No active items.")

    for index, row in active_items.iterrows():

        st.markdown("### " + row["Item Name"])
        st.write("Type:", row["Type"])
        st.write("Description:", row["Description"])
        st.write("Location:", row["Location"])
        st.write("Date:", row["Date"])
        st.write("Contact:", row["Contact"])

        # Image
        if row["Image"] == "No image uploaded":
            st.write("📷 No image uploaded")
        else:
            image_path = os.path.join(IMAGE_FOLDER, row["Image"])
            if os.path.exists(image_path):
                st.image(image_path, width=200)

        # Checkbox
        collected = st.checkbox(
            f"Item Collected - {index}",
            value=bool(row["Collected"]),
            key=f"active_{index}"
        )

        df.at[index, "Collected"] = collected

        # Delete button
        delete = st.button(
            f"🗑 Delete Post {index}",
            key=f"delete_active_{index}"
        )

        if delete:

            if row["Image"] != "No image uploaded":
                image_path = os.path.join(IMAGE_FOLDER, row["Image"])
                if os.path.exists(image_path):
                    os.remove(image_path)

            df = df.drop(index).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)

            st.rerun()

        st.markdown("---")

    # -----------------------------
    # CLAIMED ITEMS
    # -----------------------------

    st.subheader("✅ Already Claimed")

    if claimed_items.empty:
        st.info("No claimed items.")

    for index, row in claimed_items.iterrows():

        st.markdown("### " + row["Item Name"])
        st.write("Type:", row["Type"])
        st.write("Description:", row["Description"])
        st.write("Location:", row["Location"])
        st.write("Date:", row["Date"])
        st.write("Contact:", row["Contact"])

        # Image
        if row["Image"] == "No image uploaded":
            st.write("📷 No image uploaded")
        else:
            image_path = os.path.join(IMAGE_FOLDER, row["Image"])
            if os.path.exists(image_path):
                st.image(image_path, width=200)

        # Delete button
        delete = st.button(
            f"🗑 Delete Post {index}",
            key=f"delete_claimed_{index}"
        )

        if delete:

            if row["Image"] != "No image uploaded":
                image_path = os.path.join(IMAGE_FOLDER, row["Image"])
                if os.path.exists(image_path):
                    os.remove(image_path)

            df = df.drop(index).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)

            st.rerun()

        st.markdown("---")
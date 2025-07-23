import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, date

# --- Database Connection Configuration ---
DATABASE_URL = "postgresql://hritvikdadhich@localhost:5432/food_wastage_db"
engine = create_engine(DATABASE_URL)

# --- Helper Functions ---
def run_query(query, params=None):
    try:
        with engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)
        return df
    except Exception as e:
        st.error(f"Database query failed: {e}")
        return pd.DataFrame()

def execute_dml(query, params):
    try:
        with engine.connect() as connection:
            connection.execute(text(query), params)
            connection.commit()
        return True
    except Exception as e:
        st.error(f"Database operation failed: {e}")
        return False

# --- App Layout ---
st.set_page_config(layout="wide", page_title="Food Wastage Management")

st.title("🍽️ Local Food Wastage Management System")
st.write("Welcome to the system for managing surplus food and connecting providers with receivers.")

# --- DB Connection Test ---
st.sidebar.header("Connection Status")
try:
    provider_count_df = run_query("SELECT COUNT(*) FROM providers;")
    if not provider_count_df.empty:
        provider_count = int(provider_count_df.iloc[0, 0])
        st.sidebar.success(f"Connected to DB. {provider_count} providers found.")
    else:
        st.sidebar.warning("Connected to DB, but no provider count retrieved.")
except Exception as e:
    st.sidebar.error(f"DB connection failed: {e}")
    st.stop()

# --- Navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Food Listing Management"])

if page == "Dashboard":
    st.header("📊 Data Analysis & Insights")

    st.subheader("Overview Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        total_listings = run_query("SELECT COUNT(*) AS count FROM food_listings;")
        st.metric("Total Food Listings", int(total_listings.iloc[0]['count']) if not total_listings.empty else 0)
    with col2:
        total_providers = run_query("SELECT COUNT(*) AS count FROM providers;")
        st.metric("Total Providers", int(total_providers.iloc[0]['count']) if not total_providers.empty else 0)
    with col3:
        expired_items = run_query("SELECT COUNT(*) AS count FROM food_listings WHERE expiry_date < CURRENT_DATE;")
        st.metric("Expired Items", int(expired_items.iloc[0]['count']) if not expired_items.empty else 0)

    st.subheader("📌 Recent Food Listings")
    recent_listings = run_query("""
        SELECT f.food_name, f.quantity, f.expiry_date, f.location, f.food_type, f.meal_type, p.name AS provider
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.provider_id
        ORDER BY f.food_id DESC
        LIMIT 10;
    """)
    if not recent_listings.empty:
        st.dataframe(recent_listings, use_container_width=True)
    else:
        st.info("No recent listings available.")

elif page == "Food Listing Management":
    st.header("📝 Food Listing Management (CRUD)")

    st.subheader("Add New Food Listing")
    with st.form("add_food_listing_form"):
        provider_options_query = "SELECT provider_id, name, type FROM providers ORDER BY name;"
        df_providers_options = run_query(provider_options_query)

        if df_providers_options.empty:
            st.warning("No providers found in the database. Please add providers first.")
            st.stop()

        provider_name_to_id = dict(zip(df_providers_options['name'], df_providers_options['provider_id']))
        provider_name_to_type = dict(zip(df_providers_options['name'], df_providers_options['type']))
        provider_names = list(df_providers_options['name'])

        col_add1, col_add2, col_add3 = st.columns(3)
        with col_add1:
            food_name = st.text_input("Food Name", key="add_food_name")
            quantity = st.number_input("Quantity", min_value=1, value=10, key="add_quantity")
        with col_add2:
            selected_provider_name = st.selectbox("Select Provider", provider_names, index=0, key="add_provider_select")
            provider_id = provider_name_to_id.get(selected_provider_name)
            provider_type_display = provider_name_to_type.get(selected_provider_name, "")
            st.text_input("Provider Type (Auto-filled)", value=provider_type_display, disabled=True, key="add_provider_type_display")
        with col_add3:
            location_options = run_query("SELECT DISTINCT city FROM providers ORDER BY city;")['city'].tolist()
            location = st.selectbox("Location (City)", location_options, index=0, key="add_location_select")
            expiry_date = st.date_input("Expiry Date", value=date.today(), key="add_expiry_date")

        food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"], key="add_food_type_select")
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"], key="add_meal_type_select")

        submitted = st.form_submit_button("Add Listing")

        if submitted:
            if food_name and quantity and selected_provider_name and location and expiry_date and food_type and meal_type and provider_id is not None:
                insert_query = """
                INSERT INTO food_listings (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
                VALUES (:food_name, :quantity, :expiry_date, :provider_id, :provider_type, :location, :food_type, :meal_type);
                """
                params = {
                    "food_name": food_name,
                    "quantity": int(quantity),
                    "expiry_date": expiry_date,
                    "provider_id": int(provider_id),
                    "provider_type": provider_type_display,
                    "location": location,
                    "food_type": food_type,
                    "meal_type": meal_type
                }
                if execute_dml(insert_query, params):
                    st.success(f"✅ Food listing '{food_name}' added successfully!")
                    updated_listings = run_query("SELECT food_name, quantity, expiry_date, location FROM food_listings ORDER BY food_id DESC LIMIT 5;")
                    if not updated_listings.empty:
                        st.info("⬇️ Latest Added Listings:")
                        st.dataframe(updated_listings, use_container_width=True)
            else:
                st.warning("Please fill in all fields and ensure a valid provider is selected.")

    st.subheader("Delete Food Listing")
    delete_listings = run_query("SELECT food_id, food_name FROM food_listings ORDER BY food_id DESC;")
    if not delete_listings.empty:
        delete_display = delete_listings["food_id"].astype(str) + " - " + delete_listings["food_name"]
        selected_delete = st.selectbox("Select Food Listing to Delete", delete_display)
        delete_confirmed = st.button("Confirm Delete")
        if delete_confirmed:
            delete_id = int(selected_delete.split(" - ")[0])
            delete_query = "DELETE FROM food_listings WHERE food_id = :id"
            if execute_dml(delete_query, {"id": delete_id}):
                st.success("✅ Listing deleted successfully.")
                updated_listings = run_query("SELECT food_name, quantity, expiry_date, location FROM food_listings ORDER BY food_id DESC LIMIT 5;")
                if not updated_listings.empty:
                    st.info("⬇️ Updated Food Listings:")
                    st.dataframe(updated_listings, use_container_width=True)
    else:
        st.info("No listings available for deletion.")

    st.subheader("All Current Food Listings")
    all_listings = run_query("""
        SELECT f.food_id, f.food_name, f.quantity, f.expiry_date, f.location, f.food_type, f.meal_type,
               p.name AS provider_name, p.type AS provider_type
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.provider_id
        ORDER BY f.food_id DESC;
    """)
    if not all_listings.empty:
        st.dataframe(all_listings, use_container_width=True)
    else:
        st.info("No food listings found in the database.")

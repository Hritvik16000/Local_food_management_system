import pandas as pd
from sqlalchemy import create_engine, text, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# --- 1. Database Connection Configuration ---
DATABASE_URL = "postgresql://postgres:[Tc9*)Cj7]@db.zsrhjrjatcbnckpnhfau.supabase.co:5432/postgres"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:

        conn_no_db = create_engine("postgresql://hritvikdadhich@localhost:5432/postgres")
        with conn_no_db.connect() as default_conn:
            default_conn.execute(text("COMMIT")) # End any open transaction
            try:
                default_conn.execute(text(f"CREATE DATABASE food_wastage_db"))
                print("Database 'food_wastage_db' created successfully.")
            except Exception as e:
                if "already exists" in str(e):
                    print("Database 'food_wastage_db' already exists.")
                else:
                    print(f"Error creating database: {e}")
        
    print("Successfully connected to PostgreSQL.")

except Exception as e:
    print(f"Error connecting to PostgreSQL: {e}")
    print("Please ensure your PostgreSQL server (Postgres.app) is running.")
    exit() # Exit if connection fails

Base = declarative_base()

# --- 2. Define Table Schemas (SQLAlchemy ORM way for clarity) ---

class Provider(Base):
    __tablename__ = 'providers'
    provider_id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    address = Column(String)
    city = Column(String)
    contact = Column(String)

class Receiver(Base):
    __tablename__ = 'receivers'
    receiver_id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    city = Column(String)
    contact = Column(String)

class FoodListing(Base):
    __tablename__ = 'food_listings'
    food_id = Column(Integer, primary_key=True, autoincrement=True)
    food_name = Column(String)
    quantity = Column(Integer)
    expiry_date = Column(Date)
    provider_id = Column(Integer, ForeignKey('providers.provider_id'))
    provider_type = Column(String) # Stored for denormalization/convenience for queries
    location = Column(String) # This seems to map to 'City' from Provider, or could be specific
    food_type = Column(String)
    meal_type = Column(String)

class Claim(Base):
    __tablename__ = 'claims'
    claim_id = Column(Integer, primary_key=True)
    food_id = Column(Integer, ForeignKey('food_listings.food_id'))
    receiver_id = Column(Integer, ForeignKey('receivers.receiver_id'))
    status = Column(String)
    timestamp = Column(DateTime)

# --- 3. Create Tables in the Database ---
def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

# --- 4. Load Data from CSVs and Ingest into Database ---
def load_data():
    print("Loading data from CSVs...")
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Load Providers
        providers_df = pd.read_csv('providers_data.csv')
        providers_df.columns = providers_df.columns.str.lower() # ADD THIS LINE
        providers_df.to_sql('providers', engine, if_exists='append', index=False)
        print("Providers data loaded.")

        # Load Receivers
        receivers_df = pd.read_csv('receivers_data.csv')
        receivers_df.columns = receivers_df.columns.str.lower() # ADD THIS LINE
        receivers_df.to_sql('receivers', engine, if_exists='append', index=False)
        print("Receivers data loaded.")

        # Load Food Listings
        food_listings_df = pd.read_csv('food_listings_data.csv')
        food_listings_df.columns = food_listings_df.columns.str.lower() # ADD THIS LINE
        # Convert Expiry_Date to datetime objects
        food_listings_df['expiry_date'] = pd.to_datetime(food_listings_df['expiry_date']) # Note: now 'expiry_date'
        food_listings_df.to_sql('food_listings', engine, if_exists='append', index=False, dtype={'expiry_date': Date})
        print("Food Listings data loaded.")

        # Load Claims
        claims_df = pd.read_csv('claims_data.csv')
        claims_df.columns = claims_df.columns.str.lower() # ADD THIS LINE
        # Convert Timestamp to datetime objects
        claims_df['timestamp'] = pd.to_datetime(claims_df['timestamp']) # Note: now 'timestamp'
        claims_df.to_sql('claims', engine, if_exists='append', index=False, dtype={'timestamp': DateTime})
        print("Claims data loaded.")

        session.commit()
        print("All data successfully ingested.")

    except Exception as e:
        session.rollback()
        print(f"Error loading data: {e}")
    finally:
        session.close()

# --- 5. Implement Basic CRUD Operations (Functions for later use in Streamlit) ---
def get_all_food_listings():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        listings = session.query(FoodListing).all()
        return listings
    except Exception as e:
        print(f"Error fetching food listings: {e}")
        return []
    finally:
        session.close()

def add_food_listing(food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        new_listing = FoodListing(
            food_name=food_name,
            quantity=quantity,
            expiry_date=datetime.strptime(expiry_date, '%Y-%m-%d').date() if isinstance(expiry_date, str) else expiry_date,
            provider_id=provider_id,
            provider_type=provider_type,
            location=location,
            food_type=food_type,
            meal_type=meal_type
        )
        session.add(new_listing)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error adding food listing: {e}")
        return False
    finally:
        session.close()

def update_claim_status(claim_id, new_status):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        claim = session.query(Claim).filter_by(claim_id=claim_id).first()
        if claim:
            claim.status = new_status
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error updating claim status: {e}")
        return False
    finally:
        session.close()

def delete_food_listing(food_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # First, delete any claims associated with this food_id
        session.query(Claim).filter_by(food_id=food_id).delete()
        
        listing = session.query(FoodListing).filter_by(food_id=food_id).first()
        if listing:
            session.delete(listing)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error deleting food listing: {e}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    create_tables()
    load_data()
    print("\nDatabase setup and data ingestion complete.")
    print("You can now run SQL queries or the Streamlit app.")

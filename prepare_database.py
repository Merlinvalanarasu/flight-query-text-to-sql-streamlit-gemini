import pandas as pd
import sqlite3
import os

# --- Configuration ---
CSV_FILE_PATH = 'goibibo_flights_data.csv'
DB_FILE_PATH = 'flights.db'

def create_database():
    """
    Reads flight data from a CSV, normalizes it into three tables (airlines, routes, flights),
    and loads them into a new SQLite database file.
    """
    # --- Step 1: Read and Clean the Original CSV Data ---
    print("Reading the CSV file...")
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
        print("Please make sure the CSV file is in the same directory as this script.")
        return

    try:
        df = pd.read_csv(CSV_FILE_PATH)
        print("CSV data loaded successfully.")
        
        # Standardize all column names to lowercase for consistency
        df.columns = df.columns.str.lower().str.strip()
        print(f"Cleaned and standardized column names to: {df.columns.tolist()}")
        
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    # --- Step 2: Create the 'airlines' Table ---
    print("Creating 'airlines' table...")
    airlines = df['airline'].unique()
    airlines_df = pd.DataFrame(airlines, columns=['airline_name'])
    airlines_df['airline_id'] = airlines_df.index + 1
    print(f"Found {len(airlines_df)} unique airlines.")

    # --- Step 3: Create the 'routes' Table ---
    # FIX: Using the correct 'from' and 'to' columns from the CSV.
    print("Creating 'routes' table...")
    routes_df = df[['from', 'to']].drop_duplicates().reset_index(drop=True)
    # Rename for our new schema
    routes_df.rename(columns={'from': 'source', 'to': 'destination'}, inplace=True)
    routes_df['route_id'] = routes_df.index + 1
    print(f"Found {len(routes_df)} unique routes.")

    # --- Step 4: Create the Main 'flights' Table ---
    print("Preparing main 'flights' table with foreign keys...")
    flights_df = df.merge(airlines_df, left_on='airline', right_on='airline_name', how='left')
    # FIX: Merging using the original (now lowercase) column names.
    flights_df = flights_df.merge(routes_df, left_on=['from', 'to'], right_on=['source', 'destination'], how='left')

    # FIX: Selecting the correct columns that exist in the dataframe.
    # Renaming 'flight_num' to 'flight_code' for consistency.
    flights_df_final = flights_df[['flight_num', 'airline_id', 'route_id', 'dep_time', 'arr_time', 'stops', 'price']].copy()
    
    # Rename columns for consistency in the final database.
    flights_df_final.rename(columns={
        'flight_num': 'flight_code',
        'stops': 'total_stops'
    }, inplace=True)
    
    flights_df_final.insert(0, 'flight_id', range(1, 1 + len(flights_df_final)))
    print("Main 'flights' table is ready.")


    # --- Step 5: Load Data into SQLite Database ---
    print(f"Creating and connecting to the SQLite database at '{DB_FILE_PATH}'...")
    if os.path.exists(DB_FILE_PATH):
        os.remove(DB_FILE_PATH)
        print(f"Removed existing database file '{DB_FILE_PATH}'.")

    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        
        print("Writing data to database tables...")
        airlines_df[['airline_id', 'airline_name']].to_sql('airlines', conn, index=False, if_exists='replace')
        routes_df.to_sql('routes', conn, index=False, if_exists='replace')
        flights_df_final.to_sql('flights', conn, index=False, if_exists='replace')

        print("Data loaded successfully!")

    except sqlite3.Error as e:
        print(f"An error occurred with the database: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()
            print("Database connection closed.")
            print("\n--- Process Complete ---")
            print(f"Your database '{DB_FILE_PATH}' has been created successfully!")
            print("You can now proceed to the next step of building the AI query engine.")


if __name__ == '__main__':
    create_database()

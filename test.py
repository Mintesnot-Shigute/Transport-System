import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('instance/transport.db')
cursor = conn.cursor()

# Check if the table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transport_claims';")
table_exists = cursor.fetchone()

if table_exists:
    print("Table exists!")

    # Execute a query to fetch the count of rows in the transport_claims table
    cursor.execute("SELECT COUNT(*) FROM transport_claims")
    row_count = cursor.fetchone()[0]
    
    print(f"Row count: {row_count}")

    # Fetch all rows if there are any
    if row_count > 0:
        cursor.execute("SELECT * FROM transport_claims")
        rows = cursor.fetchall()

        # Print the rows
        for row in rows:
            print(row)
    else:
        print("The table is empty.")
else:
    print("Table does not exist.")

# Close the connection
conn.close()

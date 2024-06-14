import sqlite3
import os

def setup_database():
    db_path = 'signals.db'
    try:
        # Check if the database file already exists
        if not os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Model_predictions (
                    signal_id INTEGER,
                    prediction TEXT CHECK( prediction IN ('32PSK', '16APSK', '32QAM', 'FM', 'GMSK', '32APSK', 'OQPSK', '8ASK', 'Unrecognized') ) DEFAULT 'Unrecognized',
                    FOREIGN KEY(signal_id) REFERENCES Signals(id)
                )
            ''')

            # Create table for storing true labels
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS True_labels (
                    signal_id INTEGER,
                    true_label TEXT CHECK( true_label IN ('32PSK', '16APSK', '32QAM', 'FM', 'GMSK', '32APSK', 'OQPSK', '8ASK', 'Unrecognized') ) DEFAULT 'Unrecognized',
                    FOREIGN KEY(signal_id) REFERENCES Signals(id)
                )
            ''')

            conn.commit()
            conn.close()
            print(f"Database setup complete. Database created at {db_path}.")
        else:
            print(f"Database already exists at {db_path}.")
    except Exception as e:
        print(f"An error occurred while setting up the database: {e}")

if __name__ == '__main__':
    setup_database()

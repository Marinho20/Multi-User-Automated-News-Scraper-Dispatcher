from bot import run_global_bot
from scanner import runscaner
from database import connect_database
if __name__ == "__main__":
    print("🚀 BOT LOADING...")
    connection=connect_database()
    
    run_global_bot()

    # closes connection
    if connection.is_connected():
        connection.close()
        print("🔌 connection closed")
"""Setup database connection."""

from databases import Database


async def connect_to_db():
    try:
        print("Setting up database...")
        database = Database("sqlite:///app.db", echo=True)
        await database.connect()
        print("Database connected")
    except Exception as e:
        print("Error setting up database: ", e)

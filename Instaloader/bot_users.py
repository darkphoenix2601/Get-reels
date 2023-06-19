from pyrogram import Client, filters
from pyrogram.types import Message

# Create a new instance of the Client
app = Client("my_account")

# Handler for new messages
@app.on_message(filters.service, group=1)
async def handle_new_message(client: Client, message: Message):
    if not message.edit_date:
        # Your code here
        pass

# Run the application
app.run()

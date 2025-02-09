from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Statistic,DataItem
class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        dashboard_slug=self.scope['url_route']['kwargs']['dashboard_slug']
        self.dashboard_slug = dashboard_slug
        self.room_group_name = f'stats-{dashboard_slug}'
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()


    async def disconnect(self,close_code):
        print(f'connection closed with code:{close_code}')
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)



    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]

        print(message)
        print(sender)
        #print(text_data_json)
        #await self.save_data_item(sender,message)
        dashboard_slug = self.dashboard_slug

        await self.save_data_item(sender,message,dashboard_slug)
        await self.channel_layer.group_send(self.room_group_name,{
            'type':'statistics_message',
            'message':message,
            'sender':sender,
        })

    async def statistics_message(self,event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data = json.dumps({
            'message': message,
            'sender':sender,
            
        }))


    @database_sync_to_async
    def create_data_item(self,sender,message,slug):
        obj = Statistic.objects.get(slug=slug)
        return DataItem.objects.create(statistic=obj, value = message,owner = sender)
    

    async def save_data_item(self,sender,message,slug):
        await self.create_data_item(sender,message,slug)


    '''@database_sync_to_async
    def create_data_item(self, sender, message, slug):
        """Saves data to DB and returns the object."""
        obj = Statistic.objects.get(slug=slug)
        return DataItem.objects.create(statistic=obj, value=message, owner=sender)

    async def save_data_item(self, sender, message, slug):
        """Properly awaits the database function."""
        await self.create_data_item(sender, message, slug)  # No missing await'''











'''from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist  # Handle missing DB records
from .models import Statistic, DataItem

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Establish WebSocket connection."""
        dashboard_slug = self.scope["url_route"]["kwargs"]["dashboard_slug"]
        self.dashboard_slug = dashboard_slug
        self.room_group_name = f"stats-{self.dashboard_slug}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        print(f"WebSocket connected: {self.room_group_name}")

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        print(f"WebSocket closed with code: {close_code}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handle received messages from WebSocket."""
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", "").strip()
            sender = text_data_json.get("sender", "").strip()

            if not message or not sender:
                print("⚠️ Received empty message or sender. Ignoring.")
                return

            print(f"📩 Received: {message} from {sender}")

            # Save to database
            await self.save_data_item(sender, message, self.dashboard_slug)

            # Send message to WebSocket group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "statistics_message",
                    "message": message,
                    "sender": sender,
                },
            )
        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON received")
        except Exception as e:
            print(f"❌ Unexpected error in receive(): {e}")

    async def statistics_message(self, event):
        """Send messages to WebSocket clients."""
        message = event["message"]
        sender = event["sender"]

        await self.send(
            text_data=json.dumps({"message": message, "sender": sender})
        )

    @database_sync_to_async
    def create_data_item(self, sender, message, slug):
        """Create and save a new DataItem to the database."""
        try:
            obj = Statistic.objects.get(slug=slug)
            return DataItem.objects.create(statistic=obj, value=message, owner=sender)
        except ObjectDoesNotExist:
            print(f"❌ Error: No Statistic found with slug {slug}")
            return None
        except Exception as e:
            print(f"❌ Database error in create_data_item: {e}")
            return None

    async def save_data_item(self, sender, message, slug):
        """Save a DataItem asynchronously."""
        item = await self.create_data_item(sender, message, slug)
        if item:
            print(f"✅ Saved message '{message}' from {sender} to database")'''

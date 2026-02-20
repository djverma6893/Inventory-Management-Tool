from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://IMT_Equipment_DB:Imt_Mongodb%40123@equipmentinventory.kwniez6.mongodb.net/?appName=EquipmentInventory"
# client = MongoClient('mongodb+srv://IMT_Equipment_DB:Imt_Mongodb%40123@equipmentinventory.kwniez6.mongodb.net/?appName=EquipmentInventory',tls=True, tlsCAFile=certifi.where())

client = AsyncIOMotorClient(MONGO_URL)

database = client['team_equipment']   # your DB name
collection = database.equipment   # your collection

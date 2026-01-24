from pymongo import MongoClient
import certifi

# MongoDB connection URI with SSL relaxed settings
try:
    client = MongoClient(
        'mongodb+srv://IMT_Equipment_DB:Imt_Mongodb%40123@equipmentinventory.kwniez6.mongodb.net/?appName=EquipmentInventory',
        tls=True,
        tlsCAFile=certifi.where()
    )
    # Test connection
    client.admin.command('ping')
    print("✓ MongoDB connection successful!")
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    exit()

# Connect to MongoDB
# client = MongoClient(
#     MONGO_URI,
#     tls=True,
#     tlsCAFile=certifi.where()
# )

# Print all database names
databases = client.list_database_names()
db = client['team_equipment']
collection = db['equipment']
collection2= db['users']
document = {
        'team_member': "Team Member",
        'laptop1_sn': "Laptop1 SN",
        'laptop2_sn': "Laptop2 SN",
        'intern_phone': "Intern Phone",
        'test_phone1': "Test Phone 1",
        'test_phone2': "Test Phone 2",
        'hcl_laptop': "HCL Laptop",
        'serial_no': "Serial No",
    }
column_name = "charger_idfff"
# collection2.insert_one(document)
# Remove the field from all documents

result = collection.update_many(
    {column_name: {"$exists": True}},  # Only if field exists
    {"$unset": {column_name: ""}}
)
rresult = collection2.update_many(
    {column_name: {"$exists": True}},  # Only if field exists
    {"$unset": {column_name: ""}}
)
doc = collection2.find_one({"team_member":"Team Member"})
if doc:
    sk = list(doc.values())
    sk.pop(0)
    print(sk)
else:
    print("Warning: No document found with team_member='Team Member'")
data=collection.find()
data2= collection2.find()
print("Databases in MongoDB:")
for db in databases:
    print("-", db)
for db in data:
    print("-", db)
for db in data2:
    print("-", db)

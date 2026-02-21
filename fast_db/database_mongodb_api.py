import certifi
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
import hashlib
from bson.objectid import ObjectId
import requests as re
from motor.motor_asyncio import AsyncIOMotorClient


class DatabaseManager:
    def __init__(self, db_name='team_equipment'):
        """
        Initialize MongoDB connection
        :param connection_string: MongoDB connection URI
        :param db_name: Database name
        """
        MONGO_URL = "mongodb+srv://IMT_Equipment_DB:Imt_Mongodb%40123@equipmentinventory.kwniez6.mongodb.net/?appName=EquipmentInventory"
        # client = MongoClient('mongodb+srv://IMT_Equipment_DB:Imt_Mongodb%40123@equipmentinventory.kwniez6.mongodb.net/?appName=EquipmentInventory',tls=True, tlsCAFile=certifi.where())

        self.client = AsyncIOMotorClient(MONGO_URL)

        # database = client['team_equipment']  # your DB name
        # collection = database.equipment  # your collection
        # self.client = MongoClient(connection_string,tls=True, tlsCAFile=certifi.where())
        self.db = self.client[db_name]
        self.users_collection = self.db['users']
        self.equipment_collection = self.db['equipment']
        self.init_users_collection()

    def init_users_collection(self):
        """Create users collection with indexes and default users"""
        try:
            # Create unique index on username
            self.users_collection.create_index('username', unique=True)
            # Add default admin user if no users exist
            if self.users_collection.count_documents({}) == 0:
                admin_password = self.hash_password('admin123')
                self.users_collection.insert_one({
                    'username': 'admin',
                    'password': admin_password,
                    'full_name': 'Administrator',
                    'role': 'admin'
                })
                user_password = self.hash_password('user123')
                self.users_collection.insert_one({
                    'username': 'user',
                    'password': user_password,
                    'full_name': 'Members',
                    'role': 'user'
                })

        except Exception as e:
            print(f"Error initializing users collection: {e}")

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    async def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        try:
            hashed_password = self.hash_password(password)
            print("HANGI")
            user = await self.users_collection.find_one({
                'username': username,
                'password': hashed_password
            })

            if user:
                return {
                    'id': str(user['_id']),  # Convert ObjectId to string
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'role': user['role']
                }
            return None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None

    def fetch_all_records(self):
        """Fetch all equipment records"""
        try:
            records = self.equipment_collection.find()
            # records = list(re.get("http://127.0.0.1:8000/users",timeout=2).json())
            print("equipment_collection all data",records)

            # Convert ObjectId to string for compatibility
            # for record in records.json():
            # for record in records:
            #
            #     record['id'] = str(record['_id'])
            #
            #     del record['_id']
            return records
            # return records.json()
        except Exception as e:
            print(f"Error fetching records: {e}")
            return []

    def search_records(self, search_query):
        """Search equipment records by various fields"""
        try:
            # MongoDB regex search (case-insensitive)
            search_pattern = {'$regex': search_query, '$options': 'i'}

            query = {
                '$or': [
                    {'team_member': search_pattern},
                    {'serial_no': search_pattern},
                    {'laptop1_sn': search_pattern},
                    {'laptop2_sn': search_pattern},
                    {'intern_phone': search_pattern},
                    {'test_phone1': search_pattern}
                ]
            }

            records = self.equipment_collection.find(query)

            return records
        except Exception as e:
            print(f"Error searching records: {e}")
            return []

    def add_record(self, data):
        """Add a new equipment record"""
        try:
            # hnm=self.get_header_id()
            # ins_val={}
            # for id, value in zip(hnm, data):
            #     ins_val[id]=value
            self.equipment_collection.insert_one(data)
            # result = self.equipment_collection.insert_one({
            #     'team_member': data['team_member'],
            #     'laptop1_sn': data['laptop1_sn'],
            #     'laptop2_sn': data['laptop2_sn'],
            #     'intern_phone': data['intern_phone'],
            #     'test_phone1': data['test_phone1'],
            #     'test_phone2': data['test_phone2'],
            #     'hcl_laptop': data['hcl_laptop'],
            #     'serial_no': data['serial_no']
            # })
            return True
        except Exception as e:
            print(f"Error adding record: {e}")
            return False

    def update_record(self, record_id, data):
        """Update an existing equipment record"""
        try:
            print(record_id, "record id in mongodb file need to be updated")
            # hnm = self.get_header_id()
            # ins_val = {}
            # for id, value in zip(hnm, data):
            #     ins_val[id] = value
            # print(ins_val, "values need to be updated")
            result=self.equipment_collection.update_one({'_id': ObjectId(record_id)}, {'$set': data})
            # result = self.equipment_collection.update_one(
            #     {'_id': ObjectId(record_id)},
            #     {'$set': {
            #         'team_member': data['team_member'],
            #         'laptop1_sn': data['laptop1_sn'],
            #         'laptop2_sn': data['laptop2_sn'],
            #         'intern_phone': data['intern_phone'],
            #         'test_phone1': data['test_phone1'],
            #         'test_phone2': data['test_phone2'],
            #         'hcl_laptop': data['hcl_laptop'],
            #         'serial_no': data['serial_no']
            #     }}
            # )
            print(f"result {result}")
            return result
        except Exception as e:
            print(f"Error updating record: {e}")
            return False

    def delete_records(self, record_ids):
        """Delete multiple equipment records"""
        try:
            # Convert string IDs to ObjectId
            object_ids = [ObjectId(record_id) for record_id in record_ids]

            result = self.equipment_collection.delete_many({
                '_id': {'$in': object_ids}
            })
            # return result
            return result
        except Exception as e:
            print(f"Error deleting records: {e}")
            return False

    async def get_record_by_id(self, record_id):
        """Get a single equipment record by ID"""
        try:
            record = await self.equipment_collection.find_one({'_id': ObjectId(record_id)})

            if record:
                record['id'] = str(record['_id'])
                del record['_id']

            return record
        except Exception as e:
            print(f"Error fetching record: {e}")
            return None
    #get header ID name of main table
    async def get_header_id(self, header_name=None):
        if header_name:
            doc= await self.users_collection.find_one({"team_member":"Team Member"})

            keys = [k for k, v in doc.items() if v in header_name]
            print(keys,header_name, "keys for deletion of table column")

            return keys

        else:
            doc=await self.equipment_collection.find_one()
            header_name = list(doc.keys())
            header_name.remove('_id')
            return header_name
    #get header name of main table
    async def get_header_name(self):
        stu= await self.users_collection.find_one({"team_member":"Team Member"})
        stu = list(stu.values())
        stu.pop(0)
        # print(stu)
        return stu

    #add new column to the main table
    def add_new_column(self, header_name=None, header_id=None):
        """Add a new column to the equipment record"""
        self.header_id = header_id
        self.header_name = header_name

        self.equipment_collection.update_many({},                     # match all documents
    {"$set": {self.header_id: ""}})
        self.users_collection.update_one({"team_member":"Team Member"}, {"$set": {self.header_id: self.header_name}})

        # print(await self.get_header_name(), "header name in db")
        # print(self.get_header_id(), "header id in db")

    #delete selected column to main the main table
    async def del_sel_column(self,  header_name=None):
        del_col= await self.get_header_id(header_name)
        for col in del_col:
            await self.equipment_collection.update_many({col:{"$exists":True}},{"$unset":{col:""}})
            await self.users_collection.update_many({col:{"$exists":True}},{"$unset":{col:""}})



    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()
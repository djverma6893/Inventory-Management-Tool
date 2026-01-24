import certifi
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
import hashlib
from bson.objectid import ObjectId


class DatabaseManager:
    def __init__(self, connection_string="mongodb+srv://IMT_Equipment_DB:Imt_Mongodb%40123@equipmentinventory.kwniez6.mongodb.net/?appName=EquipmentInventory", db_name='team_equipment'):
        """
        Initialize MongoDB connection
        :param connection_string: MongoDB connection URI
        :param db_name: Database name
        """
        self.client = MongoClient(
            connection_string,
            tls=True,
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True,
            serverSelectionTimeoutMS=30000,
            socketTimeoutMS=30000
        )
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

    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        try:
            hashed_password = self.hash_password(password)
            print("HANGI")
            user = self.users_collection.find_one({
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
            records = list(self.equipment_collection.find())
            print(records)

            # Convert ObjectId to string for compatibility
            for record in records:

                record['id'] = str(record['_id'])

                del record['_id']
            return records
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

            records = list(self.equipment_collection.find(query))

            # Convert ObjectId to string
            for record in records:
                record['id'] = str(record['_id'])
                del record['_id']

            return records
        except Exception as e:
            print(f"Error searching records: {e}")
            return []

    def add_record(self, data):
        """Add a new equipment record"""
        try:
            result = self.equipment_collection.insert_one({
                'team_member': data['team_member'],
                'laptop1_sn': data['laptop1_sn'],
                'laptop2_sn': data['laptop2_sn'],
                'intern_phone': data['intern_phone'],
                'test_phone1': data['test_phone1'],
                'test_phone2': data['test_phone2'],
                'hcl_laptop': data['hcl_laptop'],
                'serial_no': data['serial_no']
            })
            return True
        except Exception as e:
            print(f"Error adding record: {e}")
            return False

    def update_record(self, record_id, data):
        """Update an existing equipment record"""
        try:
            result = self.equipment_collection.update_one(
                {'_id': ObjectId(record_id)},
                {'$set': {
                    'team_member': data['team_member'],
                    'laptop1_sn': data['laptop1_sn'],
                    'laptop2_sn': data['laptop2_sn'],
                    'intern_phone': data['intern_phone'],
                    'test_phone1': data['test_phone1'],
                    'test_phone2': data['test_phone2'],
                    'hcl_laptop': data['hcl_laptop'],
                    'serial_no': data['serial_no']
                }}
            )
            return result.modified_count > 0 or result.matched_count > 0
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

            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting records: {e}")
            return False

    def get_record_by_id(self, record_id):
        """Get a single equipment record by ID"""
        try:
            record = self.equipment_collection.find_one({'_id': ObjectId(record_id)})

            if record:
                record['id'] = str(record['_id'])
                del record['_id']

            return record
        except Exception as e:
            print(f"Error fetching record: {e}")
            return None
    #get header ID name of main table
    def get_header_id(self):
        doc=self.equipment_collection.find_one()
        header_name = list(doc.keys())
        header_name.remove('_id')
        return header_name
    #get header name of main table
    def get_header_name(self):
        stu= list(self.users_collection.find_one({"team_member":"Team Member"}).values())
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

        print(self.get_header_name())
        print(self.get_header_id())


    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()
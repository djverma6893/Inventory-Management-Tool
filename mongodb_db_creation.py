import certifi
from pymongo import MongoClient
import random

# Connect to MongoDB (creates database if doesn't exist)
client = MongoClient('mongodb+srv://IMT_Equipment_DB:Imt_Mongodb%40123@equipmentinventory.kwniez6.mongodb.net/?appName=EquipmentInventory',tls=True, tlsCAFile=certifi.where())
db = client['team_equipment']
collection = db['equipment']

# Clear existing data (optional - for testing)
# collection.delete_many({})

# Sample data
first_names = ['John', 'Sarah', 'Mike', 'Emily', 'David', 'Lisa', 'Tom', 'Anna',
               'Chris', 'Jessica', 'Ryan', 'Amy', 'Kevin', 'Laura', 'Daniel']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
              'Davis', 'Martinez', 'Lopez', 'Wilson', 'Anderson', 'Taylor', 'Thomas']

# Generate 30 sample records
sample_data = []
for i in range(30):
    team_member = f"{random.choice(first_names)} {random.choice(last_names)}"
    laptop1_sn = f"LT1-{random.randint(100000, 999999)}"
    laptop2_sn = f"LT2-{random.randint(100000, 999999)}" if random.random() > 0.3 else None
    intern_phone = f"+1-555-{random.randint(1000, 9999)}"
    test_phone1 = f"TP1-{random.randint(10000, 99999)}"
    test_phone2 = f"TP2-{random.randint(10000, 99999)}" if random.random() > 0.4 else None
    hcl_laptop = random.choice(['YES', 'NO'])
    serial_no = f"SN-{random.randint(1000000, 9999999)}"

    # Create document (MongoDB uses dictionaries/documents instead of tuples)
    document = {
        'team_member': team_member,
        'laptop1_sn': laptop1_sn,
        'laptop2_sn': laptop2_sn,
        'intern_phone': intern_phone,
        'test_phone1': test_phone1,
        'test_phone2': test_phone2,
        'hcl_laptop': hcl_laptop,
        'serial_no': serial_no
    }
    sample_data.append(document)

# Insert sample data
result = collection.insert_many(sample_data)

print("Database created successfully!")
print(f"Inserted {len(result.inserted_ids)} documents")

# Display the data
print("\nSample of inserted data:")
print("-" * 120)

# Fetch first 10 documents
documents = collection.find().limit(10)

# Print header
print(f"{'ID':<26} {'Team Member':<20} {'Laptop1 SN':<15} {'Laptop2 SN':<15} {'Intern Phone':<15} "
      f"{'Test Phone1':<12} {'Test Phone2':<12} {'HCL':<5} {'Serial NO':<12}")
print("-" * 120)

# Print documents
for doc in documents:
    print(f"{str(doc['_id']):<26} {doc['team_member']:<20} {doc['laptop1_sn']:<15} "
          f"{str(doc.get('laptop2_sn', 'None')):<15} {doc['intern_phone']:<15} "
          f"{doc['test_phone1']:<12} {str(doc.get('test_phone2', 'None')):<12} "
          f"{doc['hcl_laptop']:<5} {doc['serial_no']:<12}")

# Get total count
count = collection.count_documents({})
print(f"\nTotal records in database: {count}")

# Close connection
client.close()
print("\nDatabase connection closed.")
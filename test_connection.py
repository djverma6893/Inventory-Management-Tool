#!/usr/bin/env python3
"""
MongoDB Connection Diagnostic Tool
"""
import socket
import sys

# Test 1: Network connectivity
print("=" * 60)
print("STEP 1: Testing Network Connectivity")
print("=" * 60)

hosts = [
    'ac-qixhgwi-shard-00-00.kwniez6.mongodb.net',
    'ac-qixhgwi-shard-00-01.kwniez6.mongodb.net',
    'ac-qixhgwi-shard-00-02.kwniez6.mongodb.net'
]

for host in hosts:
    try:
        print(f"\nTesting {host}:27017...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, 27017))
        sock.close()
        
        if result == 0:
            print(f"  ✓ Port 27017 is OPEN (reachable)")
        else:
            print(f"  ✗ Port 27017 is CLOSED (blocked by firewall)")
    except socket.gaierror as e:
        print(f"  ✗ DNS resolution failed: {e}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

# Test 2: Python and pymongo version
print("\n" + "=" * 60)
print("STEP 2: Checking Python & PyMongo Versions")
print("=" * 60)

print(f"\nPython Version: {sys.version}")

try:
    import pymongo
    print(f"PyMongo Version: {pymongo.__version__}")
except ImportError:
    print("✗ PyMongo not installed")

try:
    import certifi
    print(f"Certifi Version: {certifi.__version__}")
    print(f"CA Bundle Path: {certifi.where()}")
except ImportError:
    print("✗ Certifi not installed")

# Test 3: MongoDB Connection Attempt
print("\n" + "=" * 60)
print("STEP 3: Testing MongoDB Connection")
print("=" * 60)

try:
    from pymongo import MongoClient
    print("\nAttempting connection (30 second timeout)...")
    
    client = MongoClient(
        'mongodb+srv://IMT_Equipment_DB:Imt_Mongodb%40123@equipmentinventory.kwniez6.mongodb.net/?appName=EquipmentInventory',
        tls=True,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000
    )
    
    # Attempt ping
    client.admin.command('ping')
    print("✓ MongoDB Connection SUCCESSFUL!")
    print("✓ Database is reachable")
    
except Exception as e:
    print(f"✗ MongoDB Connection FAILED")
    print(f"Error: {str(e)[:200]}")

print("\n" + "=" * 60)
print("Diagnostic Complete")
print("=" * 60)

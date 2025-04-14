import os
import pymongo
from pymongo.errors import OperationFailure
from pymongo.mongo_client import MongoClient
from pymongo import errors
import hashlib
from urllib.parse import quote_plus

# MongoDB connection string
# Load credentials from environment variables
username = os.getenv("MONGODB_USERNAME", "")
password = os.getenv("MONGODB_PASSWORD", "")
escaped_password = quote_plus(password)  # URL-encode the password

# Construct the connection string
MONGODB_URI = f"mongodb+srv://{username}:{escaped_password}@cluster0.8vgnq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def get_collection(bot_name, mongo_uri):
    try:
        client = MongoClient(mongo_uri)

        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        # Generate a unique collection name using the bot token
        collection_name = hashlib.md5(bot_name.encode()).hexdigest()
        db = client['Luminant']
        return db[collection_name]

    except errors.OperationFailure as e:
        raise ValueError(f"Failed to connect to MongoDB: {e}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {e}")

def save_name(collection, name):
    try:
        # Save name to local file
        with open("name.txt", "w") as file:
            file.write(name)
        
        # Check if name already exists in MongoDB
        existing_name = collection.find_one({"type": "name"})
        if existing_name:
            # Update existing name in MongoDB
            collection.update_one({"type": "name"}, {"$set": {"value": name}})
        else:
            # Insert new name into MongoDB
            collection.insert_one({"type": "name", "value": name})

    except Exception as e:
        print(f"Error saving name: {e}")

def load_name(collection):
    try:
        # Try to load name from local file
        with open("name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass  # If file not found, proceed to MongoDB
    
    try:
        # Load name from MongoDB
        result = collection.find_one({"type": "name"})
        if result:
            return result.get("value")  # Use get method to avoid KeyError
    except Exception as e:
        print(f"Error loading name: {e}")
    
    return None  # Default value if not found

def save_accept_logs(collection, accept_logs):
    try:
        # Save accept_logs to local file
        with open("accept_logs.txt", "w") as file:
            file.write(str(accept_logs))
        
        # Check if accept_logs already exists in MongoDB
        existing_logs = collection.find_one({"type": "accept_logs"})
        if existing_logs:
            # Update existing accept_logs in MongoDB
            collection.update_one({"type": "accept_logs"}, {"$set": {"value": accept_logs}})
        else:
            # Insert new accept_logs into MongoDB
            collection.insert_one({"type": "accept_logs", "value": accept_logs})

    except Exception as e:
        print(f"Error saving accept_logs: {e}")

def load_accept_logs(collection):
    try:
        # Try to load accept_logs from local file
        with open("accept_logs.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        pass  # If file not found or contains invalid data, proceed to MongoDB
    
    try:
        # Load accept_logs from MongoDB
        result = collection.find_one({"type": "accept_logs"})
        if result:
            return result.get("value", 0)  # Use get method to avoid KeyError
    except Exception as e:
        print(f"Error loading accept_logs: {e}")
    
    return 0  # Default value if not found

def save_authorized_users(collection, authorized_users):
    try:
        # Save authorized users to local file
        with open("authorized_users.txt", "w") as file:
            for user_id in authorized_users:
                file.write(str(user_id) + "\n")
        
        # Check if authorized users already exist in MongoDB
        existing_users = collection.find_one({"type": "authorized_users"})
        if existing_users:
            # Update existing authorized users in MongoDB
            collection.update_one({"type": "authorized_users"}, {"$set": {"value": authorized_users}})
        else:
            # Insert new authorized users into MongoDB
            collection.insert_one({"type": "authorized_users", "value": authorized_users})

    except Exception as e:
        print(f"Error saving authorized users: {e}")

def load_authorized_users(collection):
    try:
        # Try to load authorized users from local file
        with open("authorized_users.txt", "r") as file:
            return [int(user_id) for user_id in file.read().splitlines()]
    except (FileNotFoundError, ValueError):
        pass  # If file not found or contains invalid data, proceed to MongoDB
    
    try:
        # Load authorized users from MongoDB
        result = collection.find_one({"type": "authorized_users"})
        if result:
            return result.get("value", [])  # Use get method to avoid KeyError
    except Exception as e:
        print(f"Error loading authorized users: {e}")
    
    return []  # Default value if not found

def save_allowed_channel_ids(collection, allowed_channel_ids):
    try:
        # Save allowed channel IDs to local file
        with open("allowed_channel_ids.txt", "w") as file:
            for channel_id in allowed_channel_ids:
                file.write(str(channel_id) + "\n")
        
        # Check if allowed channel IDs already exist in MongoDB
        existing_channels = collection.find_one({"type": "allowed_channel_ids"})
        if existing_channels:
            # Update existing allowed channel IDs in MongoDB
            collection.update_one({"type": "allowed_channel_ids"}, {"$set": {"value": allowed_channel_ids}})
        else:
            # Insert new allowed channel IDs into MongoDB
            collection.insert_one({"type": "allowed_channel_ids", "value": allowed_channel_ids})

    except Exception as e:
        print(f"Error saving allowed channel IDs: {e}")

def load_allowed_channel_ids(collection):
    try:
        # Try to load allowed channel IDs from local file
        with open("allowed_channel_ids.txt", "r") as file:
            return [int(channel_id) for channel_id in file.read().splitlines()]
    except (FileNotFoundError, ValueError):
        pass  # If file not found or contains invalid data, proceed to MongoDB
    
    try:
        # Load allowed channel IDs from MongoDB
        result = collection.find_one({"type": "allowed_channel_ids"})
        if result:
            return result.get("value", [])  # Use get method to avoid KeyError
    except Exception as e:
        print(f"Error loading allowed channel IDs: {e}")
    
    return []  # Default value if not found

def save_log_channel_id(collection, log_channel_id):
    try:
        # Save log channel ID to local file
        with open("log_channel_id.txt", "w") as file:
            file.write(str(log_channel_id))
        
        # Check if log channel ID already exists in MongoDB
        existing_log_channel = collection.find_one({"type": "log_channel_id"})
        if existing_log_channel:
            # Update existing log channel ID in MongoDB
            collection.update_one({"type": "log_channel_id"}, {"$set": {"value": log_channel_id}})
        else:
            # Insert new log channel ID into MongoDB
            collection.insert_one({"type": "log_channel_id", "value": log_channel_id})

    except Exception as e:
        print(f"Error saving log channel ID: {e}")

def load_log_channel_id(collection):
    try:
        # Try to load log channel ID from local file
        with open("log_channel_id.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        pass  # If file not found or contains invalid data, proceed to MongoDB
    
    try:
        # Load log channel ID from MongoDB
        result = collection.find_one({"type": "log_channel_id"})
        if result:
            return result.get("value", -1)  # Use get method to avoid KeyError
    except Exception as e:
        print(f"Error loading log channel ID: {e}")
    
    return -1  # Default value if not found

#===================== SAVING AND LOADING BOT RUNNING TIME ===========================

def save_bot_running_time(collection, time_to_add):
    try:
        current_time = collection.find_one({"type": "bot_running_time"})
        if current_time:
            total_time = current_time['time'] + time_to_add
            collection.update_one({"type": "bot_running_time"}, {"$set": {"time": total_time}})
        else:
            total_time = time_to_add
            collection.insert_one({"type": "bot_running_time", "time": total_time})
        return total_time
    except Exception as e:
        print(f"Error saving bot running time: {e}")
        return 0

def load_bot_running_time(collection):
    try:
        current_time = collection.find_one({"type": "bot_running_time"})
        return current_time['time'] if current_time else 0
    except Exception as e:
        print(f"Error loading bot running time: {e}")
        return 0

def reset_bot_running_time(collection, new_time=0):
    try:
        collection.update_one({"type": "bot_running_time"}, {"$set": {"time": new_time}}, upsert=True)
    except Exception as e:
        print(f"Error resetting bot running time: {e}")

def save_max_running_time(collection, max_time):
    try:
        collection.update_one({"type": "max_running_time"}, {"$set": {"time": max_time}}, upsert=True)
    except Exception as e:
        print(f"Error saving max running time: {e}")

def load_max_running_time(collection):
    try:
        current_time = collection.find_one({"type": "max_running_time"})
        return current_time['time'] if current_time else 800 * 3600  # Default to 800 hours in seconds
    except Exception as e:
        print(f"Error loading max running time: {e}")
        return 800 * 3600  # Default value if not found

#============ QUEUE FILE SAVING AND LOADING ================

def save_queue_file(collection, file_queue):
    try:
        collection.delete_many({"type": "file_queue"})  # Clear existing queue
        if file_queue:
            collection.insert_one({"type": "file_queue", "file_queue_data": file_queue})  # Save queue to MongoDB
    except Exception as e:
        print(f"Error saving file queue: {e}")

def load_queue_file(collection):
    try:
        result = collection.find_one({"type": "file_queue"})
        return result['file_queue_data'] if result else []
    except Exception as e:
        print(f"Error loading file queue: {e}")
        return []

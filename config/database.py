from pymongo import MongoClient

client=MongoClient("mongodb+srv://root_daemon:f##ksociety@cluster0.j5kvnu9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client['rollbased_taskmanger']

# collection_name=db.users

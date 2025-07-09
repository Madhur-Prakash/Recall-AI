from motor.motor_asyncio import AsyncIOMotorClient

# MONGO_URI = "mongodb://localhost:27017"


MONGO_URI = "mongodb://ec2-44-222-241-47.compute-1.amazonaws.com:27017"  # --> for aws testing
mongo_client = AsyncIOMotorClient(MONGO_URI)

from langgraph.checkpoint.redis import RedisSaver
from redis  import Redis
    
def redis_checkpoint():
    redis_client = Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    checkpointer = RedisSaver(redis_client=redis_client)
    checkpointer.setup()

    return checkpointer
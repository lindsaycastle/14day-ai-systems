from limits import RateLimitItemPerMinute
from limits.storage import MemoryStorage
from limits.strategies import MovingWindowRateLimiter
 
# Initialize storage (in-memory for single process)
storage = MemoryStorage()
 
# Initialize rate limiting strategy (Moving window here)
limiter = MovingWindowRateLimiter(storage)
 
# Define the global rate limit: 10 calls per minute
one_per_minute = RateLimitItemPerMinute(10,1)

def limit():

    if limiter.hit(one_per_minute, "test_namespace", "foo") == False:
        return False
        
    else:     
        limiter.hit(one_per_minute, "test_namespace", "foo")
        return True




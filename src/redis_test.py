import asyncio

from redis.asyncio import Redis
from redis.exceptions import RedisError

redis_clint = Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

async def run_redis_demo() -> None:
    try:
        await redis_clint.ping()

        print("✅ Redis连接成功（Python异步版）")

        await redis_clint.delete(
            "demo:name",
            "demo:code",
            "demo:user:1001",
            "demo:task:list",
            "demo:tag:set",
            "demo:score:rank",
            "demo:lock:order:1001",
        )

        await redis_clint.set(
            "demo:name",
            "张三",
        )

        await redis_clint.set(
            "demo:code",
            "6666",
            ex=300,
        )

        name = await redis_clint.get("demo:name")
        code = await redis_clint.get("demo:code")
        code_ttl = await redis_clint.ttl("demo:code")

        print("String name:", name)
        print("String code:", code)
        print("String code剩余秒数:", code_ttl)

        await redis_clint.hset(
            "demo:user:1001",
            mapping={
                "name": "李四",
                "age": 28,
            },
        )

        user = await redis_clint.hgetall(
            "demo:user:1001"
        )

        print("Hash user:", user)

        await redis_clint.lpush(
            "demo:task:list",
            "任务1",
            "任务2",
        )

        await redis_clint.rpush(
            "demo:task:list",
            "任务3",
        )

        tasks = await redis_clint.lrange(
            "demo:task:list",
            0,
            -1,
        )

        print("List:", tasks)

        added_count = await redis_clint.sadd(
            "demo:tag:set",
            "redis",
            "python",
            "fastapi",
        )

        tags = await redis_clint.smembers(
            "demo:tag:set"
        )

        python_exists = await redis_clint.sismember(
            "demo:tag:set",
            "python",
        )

        print("Set新增数量:", added_count)
        print("Set全部标签:", tags)
        print("Set是否包含python:", python_exists)

        await redis_clint.zadd(
            "demo:score:rank",
            {
                "小明": 99,
                "小红": 95,
            },
        )

        ranking_ascending  = await redis_clint.zrange(
            "demo:score:rank",
            0,
            -1,
            withscores=True,
        )

        ranking_descending = await redis_clint.zrange(
            "demo:score:rank",
            0,
            -1,
            desc=True,
            withscores=True,
        )

        xiaoming_score = await redis_clint.zscore(
            "demo:score:rank",
            "小明",
        )

        print("ZSet低分到高分:", ranking_ascending)
        print("ZSet高分到低分:", ranking_descending)
        print("小明的分数:", xiaoming_score)

        lock_key = "demo:lock:order:1001"

        first_lock_result = await redis_clint.set(
            lock_key,
            "locked",
            nx=True,
            ex=10,
        )

        second_lock_result = await redis_clint.set(
            lock_key,
            "locked",
            nx=True,
            ex=10,
        )

        print(
            "第一次加锁:",
            "成功" if first_lock_result else "失败",
        )

        print(
            "第二次加锁:",
            "成功" if second_lock_result else "失败",
        )

    except RedisError as error:
        print("❌ Redis执行异常:", error)
    finally:
        await redis_clint.aclose()
        print("Redis客户端已关闭")

def main():
    asyncio.run(run_redis_demo())

if __name__ == "__main__":
    main()
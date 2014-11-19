#!/bin/sh

redis-cli -h 10.0.0.199 keys "Tianp:prize_lottery_list:*" > keys.asc
cat keys.asc | sed 's/^/redis-cli -h 10.0.0.199 get /g' | sh > vals.asc
paste -d \  keys.asc vals.asc > Tianp_redis.log
rm -f keys.asc vals.asc

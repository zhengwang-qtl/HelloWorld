import cacluteZJBdata as cZJB
#import FuncParam as Fun #蒸发冷一体机组系数（制冷工况） K
import FuncParam_84_213 as Fun #风冷热泵机组系数（制热工况） J
import time
filename='./ZJDATA84-213'
#filename='./ZJDATA2-83'
curk=1
min=15
start_time = time.time()
print('====start=====')
p = cZJB.loadp(filename)
x = cZJB.loadx(filename)
res = cZJB.makeDepthOptimizetion(Fun, x, p)
print('====end=====')
print('MAPE:',res[0] )
print('MSE:', res[1])
print('b:', res[2])
print('training took %fs!' % (time.time() - start_time))
from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

# program

search_connect()
print(getBatteryStatus())

# config_block_iq(2.44e9, 0, 40e6, 1024)
# data = acquire_block_iq(1024, 10).tolist()

# print(predict_post('http://localhost:3000/predict', data))
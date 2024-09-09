

_global_dict = {}
 
 
def set_value(key,value):
#定义一个全局变量
    _global_dict[key] = value
 
 
def get_value(key,defValue=None):
#获得一个全局变量,不存在则返回默认值
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
    
def get_value0(key,defValue=100):
#获得一个全局变量,不存在则返回默认值
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
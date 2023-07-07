from data_processing import Data

list_ModaMax = Data().get_dict()
print(len(list_ModaMax))
for shop in list_ModaMax:
    for key, value in shop.dict_many.items():
        print(key, value)
    for key, value in shop.dict_schedule.items():
        print(key, value)


y = [1,2,3,4,5,6,7,8,9,10]

def shift_left_once(lst):
    temp = lst[0]
    for index in range(len(lst) - 1):
        lst[index] = lst[index + 1]         
    lst[index + 1] = temp
    print(lst)

shift_left_once(y)
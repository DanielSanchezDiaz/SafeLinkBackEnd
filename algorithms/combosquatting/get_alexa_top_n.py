
def get_alexa_top(n):
    with open('/Users/obedababio/Documents/Spring 2021/CPSC 490/SafeLink/SafeLinkBackEnd/algorithms/combosquatting/top1m.txt', 'r') as file_read:
        lines = file_read.readlines()
        with open('/Users/obedababio/Documents/Spring 2021/CPSC 490/SafeLink/SafeLinkBackEnd/algorithms/combosquatting/topn.txt', 'w') as file_write:
            file_write.writelines(lines[:n])

get_alexa_top(10)
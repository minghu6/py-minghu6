#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import heapq

class PriorityQueue:
    def __init__(self):
        self.__queue = list()
        self.__index = 0

    def push(self, item , priority):
        heapq.heappush(self.__queue, (-priority, self.__index, item))
        self.__index += 1

    def pop(self):
        return heapq.heappop(self.__queue)[-1]

    def contains(self,item):
        return item in map(lambda x:x[-1],self.__queue)

    def isEmpty(self):
        return len(self.__queue)==0
    
    def delete(self,item):
        tmp_list=list()
        target_list=list()
        if not self.contains(item):
            raise Exception('item not exist!')
        
        #item be contained
        target_tmp=heapq.heappop(self.__queue)
        while target_tmp[-1]!=item:
            tmp_list.append(target_tmp)
            target_tmp=heapq.heappop(self.__queue)

        if self.isEmpty():
            target_list.append(target_tmp)
            
        else:
            while target_tmp[-1]==item and not self.isEmpty():
                target_list.append(target_tmp)
                target_tmp=heapq.heappop(self.__queue)

            if target_tmp[-1]==item:
                target_list.append(target_tmp)
            else:
                tmp_list.append(target_tmp)
                
        [heapq.heappush(self.__queue,target_tmp) for target_tmp in tmp_list]
        return  target_list

    def change(self,item,priority):
        '''change the priority Not Suggested use!!'''
        if not self.contains(item):
            raise Exception('item not exist!')

        else:
            target_list=self.delete(item)
            [heapq.heappush(self.__queue,
                            (-priority,each[1],each[2])) for each in target_list]


if __name__=='__main__':
    pass





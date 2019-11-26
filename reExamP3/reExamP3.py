class Queue:
    def __init__(self , _list = None):
        if _list == None :
            self._list = []
        else:
            self._list = _list
    
    def enQueue(self,data):
        self._list.append(data)
    
    def deQueue(self):
        if self._list != None:
            return self._list.pop(0)
    
    def remove(self,data):
        cnt = 0
        for i in self._list:
            if i.ID == data.ID and i.jobName == data.jobName:
                return self._list.pop(cnt)
            cnt += 1

    def addFront(self,data):
        self._list.insert(0,data)
        return data

    def __str__(self):
        _str = ''
        for i in self._list:
            _str += str(i.ID) + '\t' + str(i.jobName) + '\n'
        return _str

    def isEmpty(self):
        return self._list == []

class Company:
    class Job:
        def __init__(self,ID,jobName):
            self.ID = ID
            self.jobName = jobName
    def __init__(self):
        self.priorityQ = []
        for i in range(9):
            self.priorityQ.append(Queue())
    
    def addJob(self,ID,jobName):
        newJob = self.Job(ID,jobName)
        self.priorityQ[ (int(ID)//100)-1 ].enQueue(newJob)

    def __str__(self):
        _str = 'ID\tJob Name\n'
        for i in self.priorityQ:
            _str += str(i)
        return _str

    def getNextJob(self):
        for i in self.priorityQ:
            if not i.isEmpty():
                return i.deQueue()

    def cancelJob(self, ID , jobName):
        tmpJob = self.Job(ID,jobName)
        return self.priorityQ[(int(ID)//100)-1].remove(tmpJob)

    def urgentJob(self,ID,jobName):
        tmpJob = self.Job(ID,jobName)
        self.cancelJob(ID,jobName)
        return self.priorityQ[0].addFront(tmpJob)



def main():
    cp = Company()
    while True:
        command = input().split()
        if command[0] == 'A':
            cp.addJob(command[1],command[2])
            print('Job submitted')
        elif command [0] == 'L':
            print(cp)
        elif command [0] == 'R':
            resultJob = cp.getNextJob()
            print('ID : %s\tJob: %s start running.' % (resultJob.ID , resultJob.jobName))
        elif command [0] == 'C':
            resultJob = cp.cancelJob(command[1],command[2])
            print('ID : %s\tJob: %s has been cacelled.' % (resultJob.ID , resultJob.jobName))
        elif command [0] == 'U':
            resultJob = cp.urgentJob(command[1],command[2])
            print('ID : %s\tJob: %s has first priority.' % (resultJob.ID , resultJob.jobName))

if __name__ == '__main__':
    main()
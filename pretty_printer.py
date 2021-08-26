class PPrint:
    def __init__(self):
        pass

    def pPrint(self, res):
        for key, value in res.items():
            print(key + " : " + value)

    def pPrint_multi(self, lst):
        for item in lst:
            self.pPrint(item)
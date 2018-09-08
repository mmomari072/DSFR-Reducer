"""
----------------------------------------------------------------------------------------
This code was developed by Eng. Mohammad OMARI for the sake of cleaning windows from
unused driver backups that be stored in in the C:\Windows\System32\DriverStore\FileRepository

Date of development: 08/09/2018
Verion: 0

just run the code and the old verions will be automatically reomoved

-----------------------------------------------------------------------------------------

"""
import os,copy
def IsVersionAGreaterThanB(A,B):
    Cond=False
    for i in range(len(A)):
        if A[i]>B[i]:
            return True
        elif A[i]<B[i]:
            return False
        else:
            pass
    return Cond

class Driver:
    list = {
            }
    latest_version={}
    Keys=[
        "PublishedName",
        "DriverPackageProvider",
        "Class",
        "DriverDate_and_Version",
        "SignerName"
    ]

    def __init__(self):
        self.PublishedName=""
        self.DriverPackageProvider=""
        self.Class=""
        self.DriverDate_and_Version=""
        self.SignerName=""
        self.Date=0
        self.version=[]

        pass

    def GetData(self, L=[]):
        for i in range(len(Driver.Keys)):
            Str=""
            if L[i].find(":")>=0:
                Str=L[i][L[i].find(":")+1:].strip()
            #print(Driver.Keys[i],":",Str)
            self.__dict__[Driver.Keys[i]]=Str

            pass
        self.GetDateAndVersion()
        return self

    def ImporAll(self):
        for drv in Fun1():
            A =copy.deepcopy( self.GetData(drv) )
            if A.ID() in Driver.list:
                Driver.list[A.ID()].append(A)
                if IsVersionAGreaterThanB(A.version,Driver.latest_version[A.ID()]):
                    Driver.latest_version[A.ID()]=A.version
                    pass

            else:
                Driver.list[A.ID()]=[A]
                Driver.latest_version[A.ID()] = A.version
                pass

            pass
    def ID(self):
        return self.DriverPackageProvider+"-"+self.Class

    def GetDateAndVersion(self):
        from datetime import datetime as dt
        A=self.DriverDate_and_Version.split(" ")
        ##print(A)
        self.Date=dt.strptime(A[0].strip(),"%m/%d/%Y")
        self.version=[int(x) for x in A[1].split('.')]
        pass
    def ResetClass(self):
        Driver.list = {}
        Driver.latest_version = {}
        pass
    def RemoveFromSystem(self):
        os.system("pnputil /d %s"%self.PublishedName)
        pass

    def CleanOldVersions(self):
        self.ResetClass()
        self.ImporAll()
        for drv in Driver.list:
            if len(Driver.list[drv])<=1:
                print("-"*80)
                print("No need to remove [%s] Drviver [skipping this driver]"%(Driver.list[drv][0].ID()))
                continue
            else:
                print("*"*80)
                print("[%s] Driver has %i backups,which will be removed"%(Driver.list[drv][0].ID(),len(Driver.list[drv])-1))

            for ver in Driver.list[drv]:
                if ver.version == Driver.latest_version[drv]:
                    continue
                else:
                    ver.RemoveFromSystem()
                    pass
                pass
            pass

    pass




def Fun1():
    Str = os.popen("pnputil /e").read().split("\n")
    ##print(Str)
    List = []
    L = []
    for i in range(2, len(Str)-1):
        ##print(Str[i])
        if len(Str[i]) > 0:
            L.append(Str[i])
        else:
            List.append(L)
            L = []
            pass
        pass
    #print(List)
    #exit()
    return List





if __name__=="__main__":
    D = Driver()
    D.ImporAll()
    D.CleanOldVersions()
    for i in D.latest_version:
        #print(i, D.latest_version[i],len(D.list[i]))
        pass

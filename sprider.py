import requests
from bs4 import BeautifulSoup
import datetime, time
import threading
import os

def take_time(info):
    time = info[1]
    time = int(time.replace('-', ''))
    return time


class ReleasedInfo:
    '''
    url = 'http://tz.its.csu.edu.cn/Home/Release_TZTG/'
    '''

    def __init__(self, url= 'http://tz.its.csu.edu.cn/Home/Release_TZTG/'):
        self.url = url
        self.date = datetime.datetime.now()
        self.pages_num = 5
        self.info = None
        self.Using_MutliThreadings = False
        

    def virtual_terminal(self):
        while True:
            inputs = input('>> ').lower()
            if inputs == 'help':
                print('[Terminal]:')
                print('      help: gets help')
                print('      fetch: fetch the school released notice')
                print('      show: if you have fetched the notice before you can reshow it by this command')
                print('      renew_url: renew the inside url if you failed to get the released school notice')
                print('      pages_num: the limitation of the school notice pages')
                print('      date: get the present time')
                

            elif inputs == 'renew_url':
                new_url = input('[Terminal] New URL:')
                os.system('ping ' + str(new_url) + ' -c4')
                time.sleep(1)
                while True:
                    flag = input('[Terminal] Confirm to renew the URL? [Y/N]')
                    if flag.lower() == 'y':
                        self.url = new_url
                        break
                    elif flag.lower() == 'n':
                        break
                    else:
                        print('[Error] Command not found')


                
            elif inputs == 'fetch':
                while True:
                    flag = input('[Terminal] Using MultiThreading? [Y/N]')
                    if flag.lower() == 'y':
                        self.Using_MutliThreadings = True
                        break
                    elif flag.lower() == 'n':
                        break
                    else:
                        print('[Error] Command not found')

                self.get_all_info()
            
            elif inputs == 'show':
                if self.info == None:
                    print('[Error] Notice is empty try command \'fetch\' ')
                else:
                    self.get_released_info()
            
            elif inputs == 'date':
                print('[Terminal] ' + str(self.date))

            elif inputs == 'pages_num':
                new_pages = input('[Terminal] Please enter the pages_num:')
                try:
                    new_pages_ = int(new_pages)
                except:
                    print('[Error] The pages_num should be a interger but your input is \'' + str(new_pages) + '\'')
                    continue
                self.pages_num = new_pages_

            else:
                print('[Error] Command not found:', inputs)
                print('        Try inputs \'help\' for more helps!')
            

    def get_information(self, soup):  
        notices = soup.find(class_='trs').find_all('tr')
        info_list = []
        for notice in notices:
            info = notice.find_all('td')[3].get_text().replace('\r', '').replace('\n', '').replace(' ','').replace('\xa0', '')
            info = info + '   ' + notice.find_all('td')[6].get_text().replace('\r', '').replace('\n', '').replace(' ','')
            info_list.append(info)
        return info_list

    def get_all_info(self):
        i = 0
        info_list = []
        print('[Terminal] Fetching the information...')
        #* Single thread
        if not self.Using_MutliThreadings:
            while i < self.pages_num:
                url_i = self.url + str(i)
                print('[Terminal] Processing...(' + str(i+1) + '/' + str(self.pages_num) + ')')
                try:
                    r = requests.get(url=url_i)
                except:
                    print('[Error] Failed to fetch the website: ' + url_i)
                    break
                r.encoding = 'utf-8'
                html = r.text
                soup = BeautifulSoup(html, 'lxml')
                temp = self.get_information(soup)
                if not temp:
                    break
                else:
                    info_list.extend(temp)
                i += 1
            self.info = info_list.copy()

        else:
            #* MultiThread
            threads_pool = []
            self.info = []
            while i < self.pages_num:
                t = threading.Thread(target=self.MultiThreadFetch, args=(i, ))
                threads_pool.append(t)
                t.start()
                i += 1
            print('[Terminal] Waiting for all threads finished...')
            for t in threads_pool:
                t.join()

    def MultiThreadFetch(self, i):
        url_i = self.url + str(i)
        print('[Terminal] Starting threads(' + str(i+1) + '/' + str(self.pages_num) + ')')

        try:
            r = requests.get(url=url_i)
        except:
            print('[Error] Failed to fetch the website: ' + url_i)

        r.encoding = 'utf-8'
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        temp = self.get_information(soup)
        if not temp:
            return
        self.info.extend(temp)
        return 0
        

    def sort_by_time(self):
        rebuild_info = [[self.info[i][:-10], self.info[i][-10:]] for i in range(len(self.info))]
        rebuild_info.sort(key=take_time, reverse=True)

        return rebuild_info

    def get_released_info(self):
        processed_info = self.sort_by_time()
        print('[Terminal] Today is ' + str(self.date) + '!')
        print('[Terminal] Infomation are following:')
        for i in range(len(processed_info)):
            print('[Terminal] ' + str(i) + ': ' + processed_info[i][0] + ' ReleasedTime: ' + processed_info[i][1])

csu = ReleasedInfo()
csu.virtual_terminal()
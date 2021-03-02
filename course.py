import time
import grequests

def exception_handler(request, exception):
    print ("Request failed")
# 这里的cookie换成你自己的,随便找个可以选课的，但是时间上冲突的进行抢课，复制粘贴发起选课课的getxhrs请求头中的cookie
headers = {'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
			'cookie': 'JSESSIONID=5F7A1E72F0D85EF7D38A7BBCC8CA9513.pyxx_server2; iPlanetDirectoryPro=i2JJKfjcbfXs6lwJPS7Mdd',
			'origin':'https://yjsjy.uestc.edu.cn',
			'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

url = 'https://yjsjy.uestc.edu.cn/pyxx/pygl/pyjhxk/jhnxk'
# bjid通过审查元素第一个td得到
bjid_list=[1525369,1507100]
count = 1
req_list = []

for bjid in bjid_list:
    req_list.append(grequests.post(url=url,data={'bjid':bjid,'qz':''},headers=headers,timeout=3))

# req_list=[
#     grequests.post(url=url,data={'bjid':1524402,'qz':''},headers=headers),#学术规范与论文写作2班
#     grequests.post(url=url,data={'bjid':1533256,'qz':''},headers=headers,timeout=3),#研究生职业生涯规划与就业指导1班
#     grequests.post(url=url,data={'bjid':1525369,'qz':''},headers=headers,timeout=3),#云计算全英文
#     grequests.post(url=url,data={'bjid':1507100,'qz':''},headers=headers,timeout=3),#体育技能、欣赏与文化游泳10班
#     grequests.post(url=url,data={'bjid':1474726,'qz':''},headers=headers),#最优化理论与应用2班
#     grequests.post(url=url,data={'bjid':1469779,'qz':''},headers=headers),#随机过程及应用6班
# ] 

while(count > 0):
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    res_list = grequests.map(req_list,exception_handler=exception_handler)
    for index in res_list:
        print(index.text)
    print('当前抢课轮次:', count)
    count = count+1
    time.sleep(0.5)
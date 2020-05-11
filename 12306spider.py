from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class QiangPiao(object):
    def __init__(self):
        self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"
        self.initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
        self.serach_url = "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc"
        self.passenger_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        self.driver = webdriver.Chrome()

    def wait_input(self):
        self.from_station = input("出发地：")
        self.to_station = input("目的地：")
        #时间格式：2019-3-31
        self.depart_time = input("出发时间：")
        self.passengers = input("乘客姓名（如果有多个乘客，用英文的逗号隔开）：").split(",")
        self.trains = input("车次（如果有多个车次，用英文的逗号隔开）：").split(",")

    def _login(self):
        self.driver.get(self.login_url)
        #显示等待,EC表示期望的条件，即登录完成之后到达个人主页，判断URL是否为个人中心的URL
        WebDriverWait(self.driver,1000).until(EC.url_to_be(self.initmy_url))
        print("登录成功")

    def _order_ticket(self):
        #1.登录成功后跳转到查票的页面
        self.driver.get(self.serach_url)

        #2.等待出发地是否输入正确
        WebDriverWait(self.driver,1000).until(EC.text_to_be_present_in_element_value((By.ID,"fromStationText"),self.from_station))
        #3.等待目的地输入正确
        WebDriverWait(self.driver,1000).until(EC.text_to_be_present_in_element_value((By.ID,"toStationText"),self.to_station))
        #4.等待出发日期输入正确
        WebDriverWait(self.driver,1000).until(EC.text_to_be_present_in_element_value((By.ID,"train_date"),self.depart_time))
        #5.判断输入的信息是否输入正确，等待查询按钮是否可用
        WebDriverWait(self.driver,1000).until(EC.element_to_be_clickable((By.ID,"query_ticket")))
        #6.如果可以点击，就找到这个查询按钮之执行点击事件
        serachBtn = self.driver.find_element_by_id("query_ticket")
        serachBtn.click()
        #7.等待查询的车次信息缓冲出来
        WebDriverWait(self.driver,1000).until(EC.presence_of_element_located((By.XPATH,".//tbody[@id='queryLeftTable']/tr")))
        #8.找到没有datatran属性的tr标签，这些标签才是存储了车次信息的标签
        tr_list = self.driver.find_elements_by_xpath(".//tbody[@id='queryLeftTable']/tr[not(@style)]")
        #9.遍历所以满足条件的tr标签
        for tr in tr_list:
            self.train_number = tr.find_element_by_class_name("number").text
            if self.train_number in self.trains:
                left_ticket = tr.find_element_by_xpath(".//td[3]").text
                if left_ticket == "有" or left_ticket.isdigit:#判断是有票还是有数字
                    #找到按钮，然后执行点击事件
                    orderBtn = tr.find_element_by_class_name("btn72")
                    orderBtn.click()

                    #等待是否来到确认乘客的页面
                    WebDriverWait(self.driver,1000).until(EC.url_to_be(self.passenger_url))
                    #等待所以的乘客信息完全被加载出来
                    WebDriverWait(self.driver,1000).until(EC.presence_of_element_located((By.XPATH,".//ul[@id='normal_passenger_id']/li")))
                    #获取所有的乘客信息
                    passenger_labels = self.driver.find_elements_by_xpath(".//ul[@id='normal_passenger_id']/li/label")
                    for passenger_label in passenger_labels:
                        name = passenger_label.text
                        if name in self.passengers:
                            passenger_label.click()

                    #获取提交订单的按钮
                    submitBtn = self.driver.find_element_by_id("submitOrder_id")
                    submitBtn.click()


                    #显示等待确认订单是否出现
                    WebDriverWait(self.driver,1000).until(EC.presence_of_element_located((By.CLASS_NAME,"dhtmlx_wins_body_outer")))

                    #再来做一个等待，如果确认按钮出现，就点击执行操作
                    WebDriverWait(self.driver,1000).until(EC.presence_of_element_located((By.ID,"qr_submit_id")))

                    confirmBtn = self.driver.find_element_by_id("qr_submit_id")
                    confirmBtn.click()
                    while confirmBtn:
                        confirmBtn.click()
                        confirmBtn = self.driver.find_element_by_id("qr_submit_id")

                    return


                #顾发琛(学生)



    def run(self):
        self.wait_input()
        self._login()
        self._order_ticket()


if __name__ == '__main__':
    spider = QiangPiao()
    spider.run()
__author__ = 'unevalenniy'
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
# from urllib.error import URLError
from time import sleep
from datetime import datetime
import sys
import inspect
import unittest

TIMEOUT = 5
SERVER_IP = 'http://192.168.174.128:4723/wd/hub'
APP = '/Users/admin/Documents/Projects/infotycoon/build/iphone/build/Debug-iphonesimulator/InfoTycoon.app'
LOGIN = 'kevin.george@informationtycoon.com'
PASSWORD = '12345678'
DEBUG = False  # raise exceptions if True, otherwise continue
LOG_NAME = 'itipad_automation.log'


class ITIPAD:
    def __init__(self):
        try:
            self.driver = webdriver.Remote(SERVER_IP, desired_capabilities={'platformName': 'iOS',
                                                                            'deviceName': 'iPad',
                                                                            'app': APP})
            self.driver.implicitly_wait(20)
            self.gps_allowed = False
            sleep(TIMEOUT * 4)
        except ConnectionRefusedError as ex:  # happens when server is not available
            # TODO implement network availability check and server start logic here
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)  # inspect.stack stays for func name
            if DEBUG:
                raise
        except TypeError as ex:  # happens when Appium server have problematic response and needs restart
            # TODO implement server restart logic here
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise

    def login(self, login_name=LOGIN, password=PASSWORD):
        try:
            self.driver.find_element_by_xpath('//UIATextField[1]').send_keys(login_name)
            self.driver.find_element_by_xpath('//UIASecureTextField[1]').send_keys(password)
            self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAButton[1]').click()
            sleep(TIMEOUT * 2)
            self.driver.find_element_by_xpath('//UIAButton[1]').click()
            sleep(TIMEOUT)
            print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Logged in as "{0}"'.format(login_name))
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise

    def open_property(self, property_name='Default Property'):
        try:
            self.driver.find_element_by_xpath('//UIASearchBar[1]').send_keys(property_name+Keys.ENTER)
            sleep(TIMEOUT)
            self.driver.find_elements_by_xpath('//UIATableCell[1]')[0].click()
            print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Property "{0}" was opened'.format(property_name))
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise

    def open_inspection(self, inspection_name='Default Inspection'):
    # the crippled logic was implemented because find_elements_by_xpath('//UIATableCell') crashes Appium server
    # until this error (https://github.com/appium/appium/issues/3154) is fixed, one have to move one by one
        try:
            i = 1
            first_name = self.driver.find_element_by_xpath('//UIATableCell[{0}]'.format(str(i)))
            while 1:
                if str(first_name.get_attribute('name')).find(inspection_name) != -1:
                    first_name.click()
                    sleep(TIMEOUT * 2)
                    break
                i += 1
                first_name = self.driver.find_element_by_xpath('//UIATableCell[{0}]'.format(str(i)))
            print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Inspection "{0}" was opened'.format(inspection_name))
        except NoSuchElementException as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise

    def open_site(self, site_name='Default Site'):
        try:
            i = 1
            first_name = self.driver.find_element_by_xpath('//UIATableCell[{0}]'.format(str(i)))
            while 1:
                if str(first_name.get_attribute('name')).find(site_name) != -1:
                    first_name.click()
                    sleep(TIMEOUT * 2)
                    break
                i += 1
                first_name = self.driver.find_element_by_xpath('//UIATableCell[{0}]'.format(str(i)))
            print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Site "{0}" was opened'.format(site_name))
        except NoSuchElementException as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise

    def inspect_first_unit(self):
        start_time = datetime.now()
        try:
            print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Started inspecting first unit')
            first_unit = self.driver.find_element_by_xpath('//UIATableCell[1]')
            first_unit.click()
            sleep(TIMEOUT)

            # enter "to do" mode so inspected items automatically hide
            self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIASegmentedControl[1]/UIAButton[1]').click()
            sleep(TIMEOUT)

            item_counter = 0  # taping buttons and dates produces hidden elements, but inspecting signature element
                              # builds the list from scratch, so the counter needs to be reset on that occasion
            real_item_counter = 0
            while 1:
                item_counter += 1
                buttons = self.driver.find_elements_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[{0}]/UIAButton'.format(str(item_counter)))
                if buttons.__len__() == 0:  # done with the list
                    print(str(datetime.now())+' [INFO]['
                          + inspect.stack()[0][3]
                          + '] Unit done in {0}, {1} items were inspected'.format((datetime.now()-start_time),
                                                                                  real_item_counter))
                    return True
                elif buttons.__len__() == 1:
                    buttons[0].click()
                    sleep(2)
                    self.driver.swipe(328, 200, 440, 200)
                    # sleep(1)
                    # self.driver.swipe((328+440)/2, 200-56, (328+440)/2, 200+56)
                    # sleep(1)
                    self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAButton[2]').click()
                    # sleep(1)
                    if not self.gps_allowed:
                        self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIATableView[2]/UIATableCell[1]').click()
                        self.gps_allowed = True
                        # sleep(1)
                    self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[3]/UIAAlert[1]/UIATableView[1]/UIATableCell[1]').click()
                    sleep(1)
                    item_counter = 0
                    print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Item "Signature" was inspected')
                elif str(buttons[2].get_attribute('name')).find('Select a Date') != -1:
                    # TODO add photo

                    # TODO add comment
                    # buttons[1].click()
                    # self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAPopover[1]/UIAButton[1]').click()
                    # self.driver.tap([(100,200)])
                    # self.driver.flick(100, 200, 110, 220)
                    #
                    # self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAPopover[1]/UIATableView[1]/UIATableCell[1]/UIATextView[1]').send_keys(str(datetime.now()))
                    # self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAPopover[1]/UIAButton[1]').click()
                    # self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAPopover[1]/UIANavigationBar[1]/UIAButton[3]').click()

                    buttons[2].click()
                    # sleep(1)
                    self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAPopover[1]/UIANavigationBar[1]/UIAButton[3]').click()
                    # sleep(1)
                    if not self.gps_allowed:
                        self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIATableView[2]/UIATableCell[1]').click()
                        self.gps_allowed = True
                        # sleep(1)
                    print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Item "Date" was inspected')
                else:
                    buttons[2].click()
                    # sleep(1)
                    if not self.gps_allowed:
                        self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIATableView[2]/UIATableCell[1]').click()
                        self.gps_allowed = True
                        # sleep(1)

                    print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Item "Button" was inspected')
                real_item_counter += 1

        except NoSuchElementException as ex:
            print(str(datetime.now())+' [WARN]['
                          + inspect.stack()[0][3]
                          + '] Unit was not done! Time spent {0}, {1} items were inspected'.format((datetime.now()-start_time),
                                                                                  real_item_counter))
            print(str(datetime.now())+' [WARN]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise
            return False
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['
                          + inspect.stack()[0][3]
                          + '] Unit was not done! Time spent {0}, {1} items were inspected'.format((datetime.now()-start_time),
                                                                                  real_item_counter))
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise
            return False

    def complete_unit(self):
        try:
            self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAStaticText[2]').click()
            self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAPopover[1]/UIAActionSheet[1]/UIAButton[2]').click()
            print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Unit completed')
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise
            return False

    # sync inspection starting from units list
    def sync_inspection(self):
        try:
            self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAStaticText[2]').click()
            self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAPopover[1]/UIAActionSheet[1]/UIAButton[2]').click()
            print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Unit completed')
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise
            return False

    def close(self):
        try:
            self.driver.quit()
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise


class TestiPad(unittest.TestCase):
    def setUp(self):
        try:
            self.logfile = open(LOG_NAME, 'a', 1)
            sys.stdout = self.logfile
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise
        print('\n---------------\n'+str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Test started')
        self.ipad = ITIPAD()
        self.ipad.login()

    def tearDown(self):
        #
        # self.ipad.close()
        try:
            print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Test completed')
            self.logfile.close()
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            if DEBUG:
                raise

    # def test_inspect_building_1(self):
    #     self.ipad.open_property('Logo Test Property')
    #     self.ipad.open_inspection('12.08.2014 v.2 (Rehab report)')
    #     self.ipad.open_site('Building 1')
    #     count = 0
    #     try:
    #         self.ipad.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIASegmentedControl[2]/UIAButton[1]').click()
    #     except Exception as ex:
    #         print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
    #     while self.ipad.inspect_first_unit():
    #         count += 1
    #         self.ipad.complete_unit()
    #
    #     print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] {0} units were inspected'.format(count))
        # self.ipad.sync_inspection()

    def test_inspect_building_2(self):
        self.ipad.open_property('Logo Test Property')
        self.ipad.open_inspection('12.08.2014 v.2 (Rehab report)')
        self.ipad.open_site('Building 2')
        count = 0
        try:
            self.ipad.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIASegmentedControl[2]/UIAButton[1]').click()
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
        while self.ipad.inspect_first_unit():
            count += 1
            self.ipad.complete_unit()
            self.ipad.sync_inspection()
            self.ipad.open_site('Building 2')
        print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] {0} units were inspected'.format(count))


    # def test_inspect_building_3(self):
    #     self.ipad.open_property('Logo Test Property')
    #     self.ipad.open_inspection('12.08.2014 v.2 (Rehab report)')
    #     self.ipad.open_site('Building 3')
    #     count = 0
    #     try:
    #         self.ipad.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIASegmentedControl[2]/UIAButton[1]').click()
    #     except Exception as ex:
    #         print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
    #     while self.ipad.inspect_first_unit():
    #         count += 1
    #         self.ipad.complete_unit()
    #     print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] {0} units were inspected'.format(count))

    # def test_inspect_building_4(self):
    #     self.ipad.open_property('Logo Test Property')
    #     self.ipad.open_inspection('12.08.2014 v.2 (Rehab report)')
    #     self.ipad.open_site('Building 4')
    #     count = 0
    #     try:
    #         self.ipad.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIASegmentedControl[2]/UIAButton[1]').click()
    #     except Exception as ex:
    #         print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
    #     while self.ipad.inspect_first_unit():
    #         count += 1
    #         self.ipad.complete_unit()
    #     print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] {0} units were inspected'.format(count))
    #
    # def test_inspect_building_5(self):
    #     self.ipad.open_property('Logo Test Property')
    #     self.ipad.open_inspection('12.08.2014 v.2 (Rehab report)')
    #     self.ipad.open_site('Building 5')
    #     count = 0
    #     try:
    #         self.ipad.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIASegmentedControl[2]/UIAButton[1]').click()
    #     except Exception as ex:
    #         print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
    #     while self.ipad.inspect_first_unit():
    #         count += 1
    #         self.ipad.complete_unit()
    #     print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] {0} units were inspected'.format(count))
    #
    # def test_inspect_building_6(self):
    #     self.ipad.open_property('Logo Test Property')
    #     self.ipad.open_inspection('12.08.2014 v.2 (Rehab report)')
    #     self.ipad.open_site('Building 6')
    #     count = 0
    #     try:
    #         self.ipad.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIASegmentedControl[2]/UIAButton[1]').click()
    #     except Exception as ex:
    #         print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
    #     while self.ipad.inspect_first_unit():
    #         count += 1
    #         self.ipad.complete_unit()
    #     print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] {0} units were inspected'.format(count))
    #
    # def test_inspect_building_7(self):
    #     self.ipad.open_property('Logo Test Property')
    #     self.ipad.open_inspection('12.08.2014 v.2 (Rehab report)')
    #     self.ipad.open_site('Building 7')
    #     count = 0
    #     try:
    #         self.ipad.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIASegmentedControl[2]/UIAButton[1]').click()
    #     except Exception as ex:
    #         print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
    #     while self.ipad.inspect_first_unit():
    #         count += 1
    #         self.ipad.complete_unit()
    #     print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] {0} units were inspected'.format(count))


    # def test_basic_1(self):
    #     self.ipad.open_property('Logo Test Property')
    #     self.ipad.open_inspection('12.08.2014 v.2 (Rehab report)')
    #     self.ipad.open_site('Building 7')
    #     count = 0
    #     try:
    #         self.ipad.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIASegmentedControl[2]/UIAButton[1]').click()
    #     except Exception as ex:
    #         print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
    #     while self.ipad.inspect_first_unit():
    #         count += 1
    #         self.ipad.complete_unit()
    #
    #     print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] {0} units were inspected'.format(count))
    #     # self.ipad.sync_inspection()


if __name__ == '__main__':
    unittest.main()
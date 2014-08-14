__author__ = 'unevalenniy'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import subprocess
import unittest
import inspect
import random

APP_ADDRESS = 'https://10.10.1.41'
TIMEOUT = 1  # latency timeout, sec
LOGIN_NAME = 'kevin.george@informationtycoon.com'
LOGIN_PASSWORD = '12345678'
COMPANY_NAME = 'Lotsawa LLC'
CATEGORY_TYPES = ['General', 'Interior', 'Exterior']
GENERAL_CATEGORY_TYPES = ['Administrative', 'Leasing', 'Operations']


class ITDB:
    def __init__(self):
        try:
            self.fp = webdriver.FirefoxProfile()
            #self.fp.add_extension(extension=
            #                      "C:\\Users\\unevalenniy\\PycharmProjects\\InfoTycoonDB\\xpath_checker-0.4.4-fx.xpi")
            #  self.fp.setPreferences("browser.helperApps.neverAsk.open",mimeType);
            self.browser = webdriver.Firefox(firefox_profile=self.fp)
            self.browser.set_window_position(1920, 0)
            self.browser.set_window_size(1280, 1024)
            self.browser.implicitly_wait(15)
            self.browser.get(APP_ADDRESS)

        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def login(self):
        try:
            self.browser.find_elements_by_xpath('//input')[0].send_keys(LOGIN_NAME)
            self.browser.find_elements_by_xpath('//input')[1].send_keys(LOGIN_PASSWORD)
            self.browser.find_elements_by_xpath('//button')[0].click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' ['+inspect.stack()[0][3]+'] Error logging in:\n', ex)

    def open_company(self, name='Lotsawa LLC'):
        try:
            sleep(TIMEOUT+2)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(name)
            sleep(TIMEOUT+1)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(name)
                                               ).find_elements_by_class_name('btn')[0].click()
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_new_property(self, property_name='Default Property Name', image_name="c:\\default.png",
                            address1='Default Address 1', address2='Default Address 2', city='Default City',
                            state='A', zip_code='12345-6789', phone_number='123-456-7890', region='C',
                            community_manager='Default Manager'):
        try:
            self.browser.get('https://10.10.1.41/#/companydashboard/properties/')
            self.browser.find_element_by_xpath("//a[contains(., 'Create New')]").click()
            self.browser.find_element_by_xpath("id('name')").send_keys(property_name)

            #  select Image using AutoIT compiled script
            autoit_selectimage = subprocess.Popen(["selectimage.exe", image_name])
            self.browser.find_element_by_xpath("id('inputImage')").click()
            while autoit_selectimage.poll():
                sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('address1')").send_keys(address1)
            self.browser.find_element_by_xpath("id('address2')").send_keys(address2)
            self.browser.find_element_by_xpath("id('city')").send_keys(city)
            self.browser.find_element_by_xpath("id('state')").send_keys(state)
            self.browser.find_element_by_xpath("id('zipCode')"
                                               ).send_keys(zip_code)  # Format is 12345 or 12345-6789
            self.browser.find_element_by_xpath("id('phoneNumber')"
                                               ).send_keys(phone_number)  # Phone Number format is 123-456-7890
            self.browser.find_element_by_xpath("id('region')").send_keys(region)
            self.browser.find_element_by_xpath("id('communityManager')").send_keys(community_manager)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

# Inspections

    def create_notype_inspection(self, property_name='Default Property Name', name='Default Inspection',
                                 date='12/13/2007', description='Default Description',
                                 instructions='Default Special Instructions'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()

            self.browser.find_elements_by_xpath("//a[contains(.,'Inspections')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('name')").send_keys(name)
            self.browser.find_elements_by_xpath("//input")[3].send_keys(date)  # date in 08/20/2014 format
            self.browser.find_element_by_xpath("id('description')").send_keys(description)
            self.browser.find_element_by_xpath("id('instructions')").send_keys(instructions)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

#TODO create Due Diligence inspection

    def select_inspection_scope(self, property_name='Default Property Name', name='Default Inspection',
                                inspection_type='General', category_types=['Administrative'],
                                locations=['Site Areas']):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Inspections')]")[0].click()
            self.browser.find_elements_by_xpath("//input")[1].send_keys(name)
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//tr[contains(.,'{0}')]".format(name)
                                                )[0].find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'{0}')]".format(inspection_type))[0].click()

            if inspection_type == 'General':
                for category_type in category_types:
                    self.browser.find_elements_by_xpath("//tr[contains(.,'{0}')]".format(category_type))[0].click()
                sleep(TIMEOUT)
                self.browser.find_elements_by_xpath("id('categories')//tr")[0].click()
                self.browser.find_elements_by_xpath("//a[contains(.,'General')]")[0].click()

            elif inspection_type == 'Interior':
                sleep(TIMEOUT)
                self.browser.find_elements_by_xpath("id('interiorItems')//input")[0].click()
                sleep(TIMEOUT)
                self.browser.find_elements_by_xpath("id('categories')//input")[0].click()
                sleep(TIMEOUT)
                for location in locations:
                    self.browser.find_elements_by_xpath("id('buildings')//div[contains(.,'{0}')]//input".format(location))[0].click()
                    sleep(TIMEOUT)
                self.browser.find_elements_by_xpath("id('units')//input")[0].click()
                sleep(TIMEOUT)

            elif inspection_type == 'Exterior':
                sleep(TIMEOUT)
                self.browser.find_elements_by_xpath("id('exteriorItem')//input")[0].click()
                sleep(TIMEOUT)
                self.browser.find_elements_by_xpath("id('category')//input")[0].click()
                sleep(TIMEOUT)

                location_ids = {'Site Areas': 'siteArea', 'Buildings': 'exteriorBuilding'}
                for location in locations:
                    self.browser.find_elements_by_xpath("id('{0}')//input".format(location_ids[location]))[0].click()

            self.browser.find_elements_by_xpath("id('inspectionSetupButton')")[0].click()
            sleep(TIMEOUT)
            if self.browser.find_elements_by_xpath("id('toast-container')"):
                print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] "'+name+'" was updated')
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def delete_inspections(self, property_name='Default Property Name', names=['Default Inspection']):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Inspections')]")[0].click()
            sleep(TIMEOUT)
            if names == '*':
                while self.browser.find_elements_by_xpath("//tr[contains(.,'')]//button").__len__() > 1:
                    name = self.browser.find_elements_by_xpath("//td")[0].text
                    self.browser.find_elements_by_xpath("//tr[contains(.,'')]//button")[1].click()
                    sleep(TIMEOUT)
                    self.browser.find_elements_by_xpath("//a[contains(.,'Delete')]")[0].click()
                    sleep(TIMEOUT)
                    self.browser.find_elements_by_xpath("//button")[2].click()
                    print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] Inspection "{0}" was deleted'.format(name))
                print(str(datetime.now())+' [INFO]['+inspect.stack()[0][3]+'] All visible inspections were deleted')
                return
            else:
                for name in names:
                    self.browser.find_elements_by_xpath("//input")[0].send_keys(name)
                    sleep(TIMEOUT)
                    self.browser.find_elements_by_xpath("//tr[contains(.,'{0}')]//button".format(name))[1].click()
                    sleep(TIMEOUT)
                    self.browser.find_elements_by_xpath("//tr[contains(.,'{0}')]//a[contains(.,'Delete')]".format(name))[0].click()
                    sleep(TIMEOUT)
                    self.browser.find_elements_by_xpath("//button")[2].click()
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

# General Items

    def create_general_item_action_value(self, property_name='Default Property Name',
                                      item_name='Default Action Value General Item',
                                      action1caption='Action1', action2caption='Action2',
                                      action3caption='Action3', action4caption='Action4',
                                      action1estCost='1', action2estCost='2', action3estCost='3', action4estCost='4',
                                      csiCodeId='02', measuringUnitId='Each'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'General Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Action'+Keys.TAB)  # Action Value
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)
            self.browser.find_element_by_xpath("id('action1caption')").send_keys(action1caption)
            self.browser.find_element_by_xpath("id('action2caption')").send_keys(action2caption)
            self.browser.find_element_by_xpath("id('action3caption')").send_keys(action3caption)
            self.browser.find_element_by_xpath("id('action4caption')").send_keys(action4caption)
            self.browser.find_element_by_xpath("id('action1estCost')").send_keys(action1estCost)
            self.browser.find_element_by_xpath("id('action2estCost')").send_keys(action2estCost)
            self.browser.find_element_by_xpath("id('action3estCost')").send_keys(action3estCost)
            self.browser.find_element_by_xpath("id('action4estCost')").send_keys(action4estCost)
            self.browser.find_element_by_xpath("id('csiCodeId')").send_keys(csiCodeId)
            self.browser.find_element_by_xpath("id('measuringUnitId')").send_keys(measuringUnitId)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_general_item_survey(self, property_name='Default Property Name', item_name='Default Survey General Item',
                                   maxscore='100'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'General Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Survey'+Keys.TAB)  # Survey
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)
            self.browser.find_element_by_xpath("id('maxscore')").send_keys(maxscore)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_general_item_counter(self, property_name='Default Property Name',
                                    item_name='Default Counter General Item'):
        try:

            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'General Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Counter'+Keys.TAB)  # Counter
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_general_item_date(self, property_name='Default Property Name', item_name='Default Date General Item'):
        try:

            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'General Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Date'+Keys.TAB)  # Date
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_general_item_petty_cash(self, property_name='Default Property Name',
                                       item_name='Default Petty Cash General Item', maxscore='100'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'General Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Petty'+Keys.TAB)  # Petty Cash
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)
            self.browser.find_element_by_xpath("id('maxscore')").send_keys(maxscore)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

# Interior Items

    def create_interior_item_action_value(self, property_name='Default Property Name',
                                          item_name='Default Action Value Interior Item',
                                          action1caption='Action1', action2caption='Action2',
                                          action3caption='Action3', action4caption='Action4',
                                          action1estCost='1', action2estCost='2', action3estCost='3', action4estCost='4',
                                          dv='Action1', measureId='Each'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Interior Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Action'+Keys.TAB)  # Action Value
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)
            self.browser.find_element_by_xpath("id('action1caption')").send_keys(action1caption)
            self.browser.find_element_by_xpath("id('action2caption')").send_keys(action2caption)
            self.browser.find_element_by_xpath("id('action3caption')").send_keys(action3caption)
            self.browser.find_element_by_xpath("id('action4caption')").send_keys(action4caption)
            self.browser.find_element_by_xpath("id('action1estCost')").send_keys(action1estCost)
            self.browser.find_element_by_xpath("id('action2estCost')").send_keys(action2estCost)
            self.browser.find_element_by_xpath("id('action3estCost')").send_keys(action3estCost)
            self.browser.find_element_by_xpath("id('action4estCost')").send_keys(action4estCost)
            self.browser.find_element_by_xpath("id('dv')").send_keys(dv)
            self.browser.find_element_by_xpath("id('measureId')").send_keys(measureId)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_interior_item_counter(self, property_name='Default Property Name', item_name='Default Counter Interior Item',
                                     cost='100'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Interior Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Counter'+Keys.TAB)  # Counter
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)
            self.browser.find_element_by_xpath("id('cost')").clear()
            self.browser.find_element_by_xpath("id('cost')").send_keys(cost)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_interior_item_date(self, property_name='Default Property Name', item_name='Default Date Interior Item'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Interior Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Date'+Keys.TAB)  # Date
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_interior_item_status(self, property_name='Default Property Name', item_name='Default Status Interior Item'):
        try:

            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Interior Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Status'+Keys.TAB)  # Status
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_interior_item_passfail(self, property_name='Default Property Name',
                                      item_name='Default Pass/Fail Interior Item'):
        try:

            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Interior Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Pass'+Keys.TAB)  # Pass/Fail
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_interior_item_signature(self, property_name='Default Property Name',
                                       item_name='Default Signature Interior Item'):
        try:

            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Interior Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Sig'+Keys.TAB)  # Signature
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

# Exterior Items

    def create_exterior_item_action_value(self, property_name='Default Property Name',
                                          item_name='Default Action Value Exterior Item',
                                          action1caption='Action1', action2caption='Action2',
                                          action3caption='Action3', action4caption='Action4',
                                          action1estCost='1', action2estCost='2', action3estCost='3', action4estCost='4',
                                          csiCodeId='02', measureId='Each'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Exterior Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Action'+Keys.TAB)  # Action Value
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)
            self.browser.find_element_by_xpath("id('action1caption')").send_keys(action1caption)
            self.browser.find_element_by_xpath("id('action2caption')").send_keys(action2caption)
            self.browser.find_element_by_xpath("id('action3caption')").send_keys(action3caption)
            self.browser.find_element_by_xpath("id('action4caption')").send_keys(action4caption)
            self.browser.find_element_by_xpath("id('action1estCost')").send_keys(action1estCost)
            self.browser.find_element_by_xpath("id('action2estCost')").send_keys(action2estCost)
            self.browser.find_element_by_xpath("id('action3estCost')").send_keys(action3estCost)
            self.browser.find_element_by_xpath("id('action4estCost')").send_keys(action4estCost)
            self.browser.find_element_by_xpath("id('csiCodeId')").send_keys(csiCodeId)
            self.browser.find_element_by_xpath("id('measureId')").send_keys(measureId)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_exterior_item_counter(self, property_name='Default Property Name', item_name='Default Counter Exterior Item',
                                     cost='100'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Exterior Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Counter'+Keys.TAB)  # Counter
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)
            self.browser.find_element_by_xpath("id('cost')").clear()
            self.browser.find_element_by_xpath("id('cost')").send_keys(cost)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def create_exterior_item_date(self, property_name='Default Property Name', item_name='Default Date Exterior Item'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Exterior Items')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("id('actionTypeId')").send_keys('Date'+Keys.TAB)  # Date
            sleep(TIMEOUT)

            self.browser.find_element_by_xpath("id('name')").send_keys(item_name)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

# Categories

    def create_category(self, property_name='Default Property Name', category='General', category_name='Name',
                        category_type='Administrative'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'{0} Categories')]".format(category))[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            if category == 'General':
                self.browser.find_element_by_xpath("id('name')").send_keys('Default ' + category_type + ' ' + category +
                                                                           ' Category ' + category_name)
                self.browser.find_element_by_xpath("id('categoryType')").send_keys(category_type+Keys.TAB)
            else:
                self.browser.find_element_by_xpath("id('name')").send_keys('Default ' + category +
                                                                           ' Category ' + category_name)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//button[contains(.,'Add')]")[0].click()
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//label[contains(.,'Items')]")[0].click()
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("id('modal')//button[contains(.,'Add')]")[0].click()

        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

# Unit Configurations

    def create_unit_configuration(self, property_name='Default Property Name', uc_name='Default Unit Configuration Name',
                        bedroom_type='Studio', bathroom_type='1BA', square_footage='100'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Unit Configurations')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            self.browser.find_element_by_xpath("id('name')").send_keys(uc_name)
            self.browser.find_element_by_xpath("id('dv')").send_keys(bedroom_type)
            self.browser.find_element_by_xpath("id('st')").send_keys(bathroom_type)
            self.browser.find_element_by_xpath("id('squareFootage')").send_keys(square_footage)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)
            
# Phases

    def create_phase(self, property_name='Default Property Name', phase_name='Default Phase Name',
                        phase_year='2014'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Phases')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            self.browser.find_element_by_xpath("id('name')").send_keys(phase_name)
            self.browser.find_element_by_xpath("id('phaseYear')").send_keys(phase_year)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

# Buildings

    def create_building(self, property_name='Default Property Name', phase_name='Default Phase Name',
                        building_name='Default Building Name',
                        address1='Default Address 1', address2='Default Address 2', city='Default City',
                        state='AK', zip_code='12345'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Buildings')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            self.browser.find_element_by_xpath("id('phaseId')").send_keys(phase_name)
            self.browser.find_element_by_xpath("id('name')").send_keys(building_name)
            self.browser.find_element_by_xpath("id('address1')").send_keys(address1)
            self.browser.find_element_by_xpath("id('address2')").send_keys(address2)
            self.browser.find_element_by_xpath("id('city')").send_keys(city)
            self.browser.find_element_by_xpath("id('stateId')").send_keys(state)
            self.browser.find_element_by_xpath("id('zipCode')").send_keys(zip_code)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' [ERROR]['+inspect.stack()[0][3]+'] ', ex)

    def building_add_units(self, property_name='Default Property Name', building_name='Default Building Name',
                           name='Default Unit', unitConfigurationId='Default Unit Configuration'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Buildings')]")[0].click()
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(building_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(building_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//a[contains(.,'Units')]")[0].click()
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()
            self.browser.find_element_by_xpath("id('name')").send_keys(name)
            self.browser.find_element_by_xpath("id('unitConfigurationId')").send_keys(unitConfigurationId)






        except Exception as ex:
            print(str(datetime.now())+' ['+inspect.stack()[0][3]+'] Error :\n', ex)

    def building_add_exterior_categories(self, property_name='Default Property Name'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Buildings')]")[0].click()









            
        except Exception as ex:
            print(str(datetime.now())+' ['+inspect.stack()[0][3]+'] Error :\n', ex)

# Site Areas

    def create_site_area(self, property_name='Default Property Name', sa_name='Default Site Area Name'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Site Areas')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Create New')]")[0].click()

            self.browser.find_element_by_xpath("id('name')").send_keys(sa_name)

            self.browser.find_element_by_xpath("id('SubmitButton')").click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' ['+inspect.stack()[0][3]+'] Error creating Building:\n', ex)
            
    def site_area_add_all_categories(self, property_name='Default Property Name', sa_name='Default Site Area Name',
                                     category_type='Interior'):
        try:
            self.browser.get("https://10.10.1.41/#/companydashboard/properties/")
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//input")[0].send_keys(property_name)
            sleep(TIMEOUT)
            self.browser.find_element_by_xpath("//tr[contains(., '{0}')]".format(property_name)
                                               ).find_elements_by_class_name('btn')[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Setup')]")[0].click()
            self.browser.find_elements_by_xpath("//a[contains(.,'Site Areas')]")[0].click()
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//tr[contains(.,'{0}')]".format(sa_name)
                                                )[0].find_elements_by_class_name('btn')[0].click()
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//a[contains(.,'{0} Categories')]".format(category_type))[0].click()
            self.browser.find_elements_by_xpath("//button[contains(.,'Add {0}')]".format(category_type))[0].click()
            sleep(TIMEOUT)
            self.browser.find_elements_by_xpath("//label[contains(.,'All {0}')]".format(category_type))[0].click()
            self.browser.find_elements_by_xpath("//button[contains(.,'Add Categories')]")[0].click()
            sleep(TIMEOUT)
        except Exception as ex:
            print(str(datetime.now())+' ['+inspect.stack()[0][3]+'] Error :\n', ex)


class TestSyncDB(unittest.TestCase):
    def setUp(self):
        self.itdb = ITDB()
        self.itdb.login()
        self.itdb.open_company()

    def test_create_new_property(self):
        self.itdb.create_new_property()

    def test_fill_items(self):
        self.itdb.create_general_item_action_value()
        self.itdb.create_general_item_counter()
        self.itdb.create_general_item_date()
        self.itdb.create_general_item_petty_cash()
        self.itdb.create_general_item_survey()

        # self.itdb.create_interior_item_action_value()
        # self.itdb.create_interior_item_counter()
        # self.itdb.create_interior_item_date()
        # self.itdb.create_interior_item_passfail()
        # self.itdb.create_interior_item_status()
        # self.itdb.create_interior_item_signature()
        #
        # self.itdb.create_exterior_item_action_value()
        # self.itdb.create_exterior_item_counter()
        # self.itdb.create_exterior_item_date()

    def test_create_and_fill_categories(self):
        for category in CATEGORY_TYPES:
            if category == 'General':
                for general_category_type in GENERAL_CATEGORY_TYPES:
                    self.itdb.create_category(category=category, category_type=general_category_type)
            else:
                self.itdb.create_category(category=category)

    def test_fill_unit_configuration(self):
        for i in range(5):
            self.itdb.create_unit_configuration(uc_name='Unit Configuration '+str(i+1), bedroom_type=str(i+1),
                                                square_footage=str((i+1)*100))

    def test_fill_phases(self):
        for i in ['2010', '2011', '2012', '2013', '2014']:
            self.itdb.create_phase(phase_name='Phase '+i, phase_year=i)

    def test_create_building(self):
        for i in range(20):
            self.itdb.create_building(building_name='Building ' + str(i + 1).zfill(3),
                                      phase_name='Phase 201' + str(random.randint(0, 4)))

    def test_create_and_fill_site_area(self):
        self.itdb.create_site_area()
        for i in ['Interior', 'Exterior']:
            self.itdb.site_area_add_all_categories(category_type=i)

    # def test_create_and_fill_notype_inspections(self):
    #     for i in GENERAL_CATEGORY_TYPES:
    #         self.itdb.create_notype_inspection(name=i+' Inspection')
    #         self.itdb.select_general_inspection_scope(name=i+' Inspection', category_types=[i])

#TODO create inspection (interior items and Building) x57-68, 139-141
    def test_interior_and_buildings_inspections(self):
        start = 57
        end = 68
        for i in range(end - start + 1):
            self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' interior items and Building Inspection')
            self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' interior items and Building Inspection',
                                              inspection_type='Interior', locations=['Buildings'])

        start = 139
        end = 141
        for i in range(end - start + 1):
            self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' interior items and Building Inspection')
            self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' interior items and Building Inspection',
                                              inspection_type='Interior', locations=['Buildings'])

    def test_exterior_and_buildings_inspections(self):
        # start = 69
        # end = 88
        # for i in range(end - start + 1):
        #     self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' exterior items and Building Inspection')
        #     self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' exterior items and Building Inspection',
        #                                       inspection_type='Exterior', locations=['Buildings'])

        start = 142
        end = 144
        for i in range(end - start + 1):
            self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' exterior items and Building Inspection')
            self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' exterior items and Building Inspection',
                                              inspection_type='Exterior', locations=['Buildings'])

#TODO create inspection (general items and general category "Administrative" type) x89-100, 145-147
    def test_gi_and_gc_administrative_inspections(self):
        # for i in range(100 - 89 + 1):
        #     self.itdb.create_notype_inspection(name=str(i + 89).zfill(3) +
        #             ' general items and general category Administrative Inspection')
        #     self.itdb.select_general_inspection_scope(name=str(i + 89).zfill(3) +
        #             ' general items and general category Administrative Inspection', category_types=['Administrative'])
        start = 145
        end = 147
        for i in range(end - start + 1):
            self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' general items and general category Administrative Inspection')
            self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' general items and general category Administrative Inspection',
                                              inspection_type='General', category_types=['Administrative'])

    def test_gi_and_gc_operations_inspections(self):
        start = 101
        end = 112
        for i in range(end - start + 1):
            self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' general items and general category Operations Inspection')
            self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' general items and general category Operations Inspection',
                                              inspection_type='General', category_types=['Operations'])

        start = 148
        end = 150
        for i in range(end - start + 1):
            self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' general items and general category Operations Inspection')
            self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' general items and general category Operations Inspection',
                                              inspection_type='General', category_types=['Operations'])

    def test_gi_and_gc_leasing_inspections(self):
        # start = 113
        # end = 132
        #
        # for i in range(end - start + 1):
        #     self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' general items and general category Leasing Inspection')
        #     self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' general items and general category Leasing Inspection',
        #                                       inspection_type='General', category_types=['Leasing'])

        start = 130
        end = 132

        for i in range(end - start + 1):
            self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' general items and general category Leasing Inspection')
            self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' general items and general category Leasing Inspection',
                                              inspection_type='General', category_types=['Leasing'])

#TODO create inspection (interior items and site area) x133-135

    def test_interior_and_site_inspections(self):
        start = 133
        end = 135

        for i in range(end - start + 1):
            self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' interior items and site area Inspection')
            self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' interior items and site area Inspection',
                                              inspection_type='Interior')

#TODO create inspection (exterior items and site area) x136-138

    def test_exterior_and_site_inspections(self):
        start = 136
        end = 138

        for i in range(end - start + 1):
            self.itdb.create_notype_inspection(name=str(i + start).zfill(3) + ' exterior items and site area Inspection')
            self.itdb.select_inspection_scope(name=str(i + start).zfill(3) + ' exterior items and site area Inspection',
                                              inspection_type='Exterior')

    def test_delete_inspections(self):
        self.itdb.delete_inspections(names='*')

    def tearDown(self):
        self.itdb.browser.quit()


if __name__ == '__main__':
    unittest.main()



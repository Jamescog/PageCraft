import unittest
from appium import webdriver
# Import Appium UiAutomator2 driver for Android platforms (AppiumOptions)

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Samsung S7',
    appPackage='com.android.settings',
    appActivity='.Settings',
    language='en',
    locale='US'
)

driver = webdriver.Remote('http://localhost:4723/wd/hub', capabilities)

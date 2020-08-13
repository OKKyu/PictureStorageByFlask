#!python3
# -*- coding:utf-8 -*-
import os
import shutil
import glob
import copy
import re
import unittest
import requests

#Test Setting
DOMAIN_STR = 'https://moloheyer:5002'
CORRECT_FILE_PATH = {'jpg':'test_img.jpg' , 'png':'test_img.png', 'gif':'test_img.gif', 'jpeg':'test_img.jpeg', 'bmp':'test_img.bmp' }
OUTPUT_PATH = '../data'

class Test_pic_post_form(unittest.TestCase):
    '''
      testing pic_post_form method.
    '''
    files = {}
    
    def setUp(self):
        '''
          load test image.
        '''
        
        #load target file
        for key, val in CORRECT_FILE_PATH.items():
            fileName = val
            fileDataBinary = None
            MIMETYPE = 'image/*'
            
            with open(fileName, 'rb') as f:
                fileDataBinary = f.read()
            self.files.setdefault(key, {'picture': (fileName, fileDataBinary, MIMETYPE)})
        
        #if target url is https, set environment variable with certification file.
        if 'https' in DOMAIN_STR:
            os.environ.setdefault('REQUESTS_CA_BUNDLE', '../env/certfile.crt')
        
        
    def testcase1(self):
        '''
          if request is sended with fileBinary and fileName correctly,
            1) return success message by json
            2) status_code is success code(200)
            3) to save into data directory
        '''
        
        #preprocess: cleanup data directory.
        shutil.rmtree(OUTPUT_PATH)
        os.mkdir(OUTPUT_PATH)
        
        #send request
        response = requests.post(DOMAIN_STR + '/pic_post_form', files=self.files.get('jpg'))
        #if set verify=False, no occured SSLError. instead of, TLS Cert has no work, not secure.
        
        #test
        self.assertEqual(type(response.json()) is dict, True)
        self.assertEqual('success' in response.json().get('result'), True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(os.path.exists(os.path.join(OUTPUT_PATH, CORRECT_FILE_PATH.get('jpg'))), True)
        
        
    def testcase2(self):
        '''
          if same name file has be sended, recent file is renamed that it is added "_number" between name and extension.
            1) duplicate 2 times.
            2) duplicate 3 times.
            3) duplicate 10 times.
        '''
        
        #duplicate 2 times.
        shutil.rmtree(OUTPUT_PATH)
        os.mkdir(OUTPUT_PATH)
        for i in range(2):
            response = requests.post(DOMAIN_STR + '/pic_post_form', files=self.files.get('jpg'))
        
        #count up sended files num. if num of data directory's file is equals sended requests num, is correct.
        sended_files = glob.glob(OUTPUT_PATH + os.sep + '*')
        self.assertEqual(len(sended_files), 2)
        
        #duplicate 3 times.
        shutil.rmtree(OUTPUT_PATH)
        os.mkdir(OUTPUT_PATH)
        for i in range(3):
            response = requests.post(DOMAIN_STR + '/pic_post_form', files=self.files.get('jpg'))
        
        #same test as duplicate 2 times.
        sended_files = glob.glob(OUTPUT_PATH + os.sep + '*')
        self.assertEqual(len(sended_files), 3)
        
        #duplicate 10 times.
        shutil.rmtree(OUTPUT_PATH)
        os.mkdir(OUTPUT_PATH)
        for i in range(10):
            response = requests.post(DOMAIN_STR + '/pic_post_form', files=self.files.get('jpg'))
        
        #same test as duplicate 2 times.
        sended_files = glob.glob(OUTPUT_PATH + os.sep + '*')
        self.assertEqual(len(sended_files), 10)
        
        
    def testcase3(self):
        '''
          These files that have some specific extension is allowed to store.
            1) File that name with allowed extension is allowed store.
            2) File that name with other is prohibited store.
        '''
        
        #allowed extension files
        shutil.rmtree(OUTPUT_PATH)
        os.mkdir(OUTPUT_PATH)
        for key in CORRECT_FILE_PATH.keys():
            response = requests.post(DOMAIN_STR + '/pic_post_form', files=self.files.get(key))
        
        sended_files = glob.glob(OUTPUT_PATH + os.sep + '*')
        self.assertEqual(len(sended_files), len(CORRECT_FILE_PATH.keys()))
        
        #disallowed extension files
        other_files = glob.glob('.' + os.sep + '*')
        for item in other_files:
            if item not in CORRECT_FILE_PATH.values() and os.path.isdir(item) == False:
                fileName = item
                fileDataBinary = None
                MIMETYPE = '*/*'
                
                with open(fileName, 'rb') as f:
                    fileDataBinary = f.read()
                response = requests.post(DOMAIN_STR + '/pic_post_form', files={'picture': (fileName, fileDataBinary, MIMETYPE)})
        
        #if disallowed file is sended and server have excluded it, output directory's count has same.
        self.assertEqual(len(sended_files), len(CORRECT_FILE_PATH.keys()))
        
    def testcase4(self):
        '''
            Test of situation that bad request is sended from client.
                1)Requests have no file.
                  It shoud be returned json message with error code 400. And Nothing to output directory.
                2)Requests have file but no finename.
                  It shoud be returned json message with error code 400. And Nothing to output directory.
        '''
        
        #prepared processing.
        shutil.rmtree(OUTPUT_PATH)
        os.mkdir(OUTPUT_PATH)
        
        #send request without file.
        response = requests.post(DOMAIN_STR + '/pic_post_form', files={'picture': (CORRECT_FILE_PATH.get('jpg'), None, 'image/*')})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(type(response.json()) is dict, True)
        self.assertEqual('Nothing uploaded file' in response.json().get('result'), True)
        self.assertEqual(len(glob.glob(OUTPUT_PATH + os.sep + '*')), 0)
        
        #send request without filename.
        binary = self.files.get('jpg')['picture'][1]
        response = requests.post(DOMAIN_STR + '/pic_post_form', files={'picture': ('', binary, 'image/*')})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(type(response.json()) is dict, True)
        self.assertEqual('Filename is not inputed' in response.json().get('result'), True)
        self.assertEqual(len(glob.glob(OUTPUT_PATH + os.sep + '*')), 0)
        
if __name__ == '__main__':
    unittest.main()

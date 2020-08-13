#!python3
# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path
import logging.config
from flask import Flask, request, jsonify
app = Flask(__name__)

#app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', 'jpeg', 'bmp']
app.config['UPLOAD_PATH'] = 'data'

@app.route("/pic_post_form", methods=["POST"])
def pic_post_form():
    app.logger.info('pic_post_form start. request was sended from ' + request.remote_addr)
    
    try:
        '''
          validation check HttpRequest
        '''
        if request.files.get('picture',None) is None:
            app.logger.warn('Nothing uploaded file.')
            return app.make_response(jsonify({'result':'Nothing uploaded file. Please send file.'})) , 400
        
        pic = request.files['picture']
        fileName = pic.filename
        if '' == fileName:
            app.logger.warn('Filename is not inputed')
            return app.make_response(jsonify({'result':'Filename is not inputed. Please input filename'})) , 400
        
        '''
          check internal directory and filename
        '''
        save_path = Path(os.path.join(app.config['UPLOAD_PATH'], fileName))
        if save_path.exists() == True:
            name_stem = save_path.stem
            extension = save_path.suffix
            count = 1
            
            while True:
                save_path = Path(os.path.join(app.config['UPLOAD_PATH'], name_stem + '_' + str(count) + extension))
                if save_path.exists() == False:
                    break
                else:
                    count = count + 1
                
        app.logger.debug('get file name is:' + fileName)
        app.logger.debug('save file name is:' + str(save_path))
        
        '''
          save file into server
        '''
        pic.save(str(save_path))
        app.logger.info('pic_post_form end succesfully for ' + request.remote_addr)
        
        return app.make_response(jsonify({'result':'file save is success'})) , 200
    
    except Exception as ex:
        app.logger.error(ex)
        return  app.make_response(jsonify({'result':'error has occured.'})) , 500

if __name__ == '__main__':
    #using log.conf for develop mode.
    logging.config.fileConfig(fname='env/log_develop.conf', disable_existing_loggers=False)
    app.run(host='192.168.1.24', port=5002)
else:
    #using log.conf for deploy mode.
    logging.config.fileConfig(fname='env/log_honban.conf', disable_existing_loggers=False)
    
app.logger.info('PictureStorage is running')
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import websocket as ws
from datetime import datetime
from time import sleep

class WSLightClient:
    
    def __init__(self):

        self.repeatFlag = True
        
        ws.enableTrace(False)

        # xxxxxxx is your name of Bluemix site.
        # yyyyyyy is url in websocket setting of node-RED
        app = ws.WebSocketApp('ws://xxxxxxxx.mybluemix.net/yyyyyyyy',
                                     on_open=self.on_open,
                                     on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        

        # Start to connect websocket.
        # Press Ctrl+C if websocket is disconnected.
        try:
            app.run_forever()
        except KeyboardInterrupt:
            app.close()

    # Receive message
    def on_message(self, wsApp, message):
        data = message

        # irsend when message is equal to command.
        if data == 'off':
            os.system("irsend SEND_ONCE light off")
        elif data == 'on':
            os.system("irsend SEND_ONCE light on")
        elif data == 'maxon':
            os.system("irsend SEND_ONCE light maxon")
        elif data == 'minon':
            os.system("irsend SEND_ONCE light minon")
        elif data == 'up':
            os.system("irsend SEND_ONCE light up")
        elif data == 'down':
            os.system("irsend SEND_ONCE light down")
        else:
            print "error"
        
        print data

    # occur error
    def on_error(self, wsApp, error):
        print 'on_error'

        print str(error)
        # Reconnect websocket when connection is closed.
        if 'Connection is already closed.' in str(error):
            self.repeatFlag = False
            print datetime.now().strftime("%y%m%d %H:%M:%S") + " True"
            
    # Close websocket
    def on_close(self, wsApp):
        print 'disconnected streaming server'
        if self.get_repeat_flag() is False:
            sleep(2)
            WSLightClient()

    # Open websocket
    def on_open(self, wsApp):
        print 'connected streaming server'

    def get_repeat_flag(self):
        return self.repeatFlag

if __name__ == "__main__":
    wslightclient = WSLightClient()

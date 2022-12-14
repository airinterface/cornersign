#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from dotenv import load_dotenv
# Loading up the values
load_dotenv()



libdir = os.getenv('E_PAPER_LIB_DIR')
picdir = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(libdir):
    sys.path.append(libdir)

import urllib
import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from display_module.subway import load_data;

logging.basicConfig(level=logging.DEBUG)
paused = False;
try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font80 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 80)

    while not paused: 
        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...")
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        dataset = load_data();
        top = 1;
        left = 5;
        listIndent = 100;
        if( dataset ):
            logging.info("-----------------------")
            logging.info( dataset )
            for item in dataset:
                if( item['type'] == 'title'):
                    draw.text((left, top), item['text'], font = font80, fill = 0)
                    top += 100
                elif ( item['type'] == 'listItem'):
                    draw.text((left + listIndent, top), item['text'], font = font24, fill = 0)
                    top += 50
        epd.display(epd.getbuffer(Himage))
        time.sleep(30)

    # logging.info("Clear...")
    # epd.init()
    # epd.Clear()

    # logging.info("Goto Sleep...")
    # epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    paused = True
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()

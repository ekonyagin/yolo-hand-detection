from ximea import xiapi
from config import camera_cfg
import numpy as np

class xi_camera_():
    def __init__(self, dev_id=0):
        try:
            self.cam = xiapi.Camera(dev_id=dev_id)
            self.cam.open_device()
            self.cam.set_imgdataformat(camera_cfg.CAMERA_PARAMS['img_format'])
            self.cam.set_exposure(camera_cfg.CAMERA_PARAMS['exposure'])
            self.cam.set_param("gain", camera_cfg.CAMERA_PARAMS['gain'])
            self.cam.set_param("auto_wb", camera_cfg.CAMERA_PARAMS['auto_wb'])
            self.cam.set_param("framerate", camera_cfg.CAMERA_PARAMS['framerate'])
            self.status = 0
        except Exception as e:
            print(f"XI_PROCESSOR: Unable to launch camera! Error is: {e}. Aborting")
            exit(-1)
        print("XI_PROCESSOR: Camera configuration finished successfully!\n")
        self.img = xiapi.Image()
    
    def start(self):
        print("XI_PROCESSOR: Starting acquisition...\n")
        self.cam.start_acquisition()
        self.status = 1
    
    def stop(self):
        print("XI_PROCESSOR: Stopping acquisition...\n")
        self.cam.stop_acquisition()
        self.status = 0
    
    def __del__(self):
        if self.status == 1:
    	    self.cam.stop_acquisition()
        self.cam.close_device()

    def get_img(self):
        self.cam.get_image(self.img)
        frame = self.img.get_image_data_numpy()[camera_cfg.CAMERA_PARAMS["offset_Y"]: \
        camera_cfg.CAMERA_PARAMS["offset_Y"]+ camera_cfg.CAMERA_PARAMS["height"],
                    camera_cfg.CAMERA_PARAMS["offset_X"]: \
                    camera_cfg.CAMERA_PARAMS["offset_X"]+ camera_cfg.CAMERA_PARAMS["width"]]
        return frame
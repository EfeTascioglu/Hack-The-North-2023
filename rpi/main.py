''' Demonstrates how to subscribe to and handle data from gaze and event streams '''
import numpy as np
import cv2

import time

import adhawkapi
import adhawkapi.frontend

from display_driver import DisplayDriver, DisplayOperation
from queue import Queue

left_wink_counter = 0
right_wink_counter = 0
left_wink = False
right_wink = False

wink_thresh = 8
class FrontendData:
    ''' BLE Frontend '''

    def __init__(self):
        # Instantiate an API object
        # TODO: Update the device name to match your device
        self._api = adhawkapi.frontend.FrontendApi(ble_device_name='ADHAWK MINDLINK-287')

        # Tell the api that we wish to receive eye tracking data stream
        # with self._handle_et_data as the handler
        self._api.register_stream_handler(adhawkapi.PacketType.EYETRACKING_STREAM, self._handle_et_data)

        # Tell the api that we wish to tap into the EVENTS stream
        # with self._handle_events as the handler
        self._api.register_stream_handler(adhawkapi.PacketType.EVENTS, self._handle_events)

        # Start the api and set its connection callback to self._handle_tracker_connect/disconnect.
        # When the api detects a connection to a MindLink, this function will be run.
        self._api.start(tracker_connect_cb=self._handle_tracker_connect,
                        tracker_disconnect_cb=self._handle_tracker_disconnect)

    def shutdown(self):
        '''Shutdown the api and terminate the bluetooth connection'''
        self._api.shutdown()

    @staticmethod
    def _handle_et_data(et_data: adhawkapi.EyeTrackingStreamData):
        ''' Handles the latest et data '''
        if et_data.gaze is not None:
            xvec, yvec, zvec, vergence = et_data.gaze
            #print(f'Gaze={xvec:.2f},y={yvec:.2f},z={zvec:.2f},vergence={vergence:.2f}')
            global gaze
            gaze = (xvec, yvec, zvec)

        if et_data.eye_center is not None:
            global left_wink_counter, right_wink_counter, left_wink, right_wink
            rxvec, ryvec, rzvec, lxvec, lyvec, lzvec = et_data.eye_center
            left_nan = np.isnan(lxvec)
            right_nan = np.isnan(rxvec)

            if left_nan and right_nan:
                left_wink_counter = 0
                right_wink_counter = 0
            elif not left_nan and not right_nan:
                if left_wink_counter > wink_thresh:
                    left_wink = True
                    left_wink_counter = 0
                if right_wink_counter > wink_thresh:
                    right_wink = True
                    right_wink_counter = 0
            elif left_nan:
                left_wink_counter += 1
            elif right_nan:
                right_wink_counter += 1

    def _handle_tracker_connect(self):
        print("Tracker connected")
        self._api.set_et_stream_rate(30, callback=lambda *args: None) #MUST BE 30 et_stream_rate!!!

        self._api.set_et_stream_control([
            adhawkapi.EyeTrackingStreamTypes.GAZE,
            adhawkapi.EyeTrackingStreamTypes.EYE_CENTER,
        ], True, callback=lambda *args: None)

    def _handle_tracker_disconnect(self):
        print("Tracker disconnected")


def main():
    ''' App entrypoint '''
    cam_mat = np.array([
        [562.85992723, 0, 328.00336446],
        [0, 562.82866525, 216.53447402],
        [0, 0, 1]
    ])
    cam_distort = np.array([
        0.10711032, -0.30212805, -0.00045349, 0.00456896, 0.24487412
    ])

    disp_queue = Queue()
    disp_thread = DisplayDriver(disp_queue)
    disp_thread.setDaemon(True)
    disp_thread.start()

    frontend = FrontendData()
    cap = cv2.VideoCapture(0)

    global left_wink, right_wink
    try:
        while True:
            if left_wink:
                print("left wink")
                left_wink = False
                disp_queue.put_nowait(DisplayOperation(DisplayOperation.Type.BLINK, 255, 0, 0))
            if right_wink:
                print("right_wink")
                right_wink = False
                disp_queue.put_nowait(DisplayOperation(DisplayOperation.Type.BLINK, 0, 0, 255))

            ret, frame = cap.read()
            if not ret:
                break
            if not np.isnan(gaze[0]):
                global gaze_coords
                gaze_coords = np.array([gaze[0], -gaze[1], -gaze[2]])
                img_pts, jac = cv2.projectPoints(gaze_coords, np.eye(3), np.array([0.0, 0.0, 0.0]), cam_mat, cam_distort)
                frame = cv2.circle(frame, img_pts[0][0].astype(int), 5, (0, 0, 255), thickness=-1)


            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        frontend.shutdown()

if __name__ == '__main__':
    main()

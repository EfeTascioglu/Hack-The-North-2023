''' Demonstrates how to subscribe to and handle data from gaze and event streams '''

import time

import adhawkapi
import adhawkapi.frontend

import cv2
import numpy as np

gaze = (0, 0, 0)

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
        #print(self._api.start_video_stream("192.168.0.1", 62829))
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
            print(f'Gaze={xvec:.2f},y={yvec:.2f},z={zvec:.2f},vergence={vergence:.2f}')
            global gaze
            gaze = (xvec, yvec, zvec)

    @staticmethod
    def _handle_events(event_type, timestamp, *args):
        if event_type == adhawkapi.Events.BLINK:
            duration = args[0]
            print(f'Got blink: {timestamp} {duration}')
        if event_type == adhawkapi.Events.EYE_CLOSED:
            eye_idx = args[0]
            print(f'Eye Close: {timestamp} {eye_idx}')
        if event_type == adhawkapi.Events.EYE_OPENED:
            eye_idx = args[0]
            print(f'Eye Open: {timestamp} {eye_idx}')

    def _handle_tracker_connect(self):
        print("Tracker connected")
        self._api.set_et_stream_rate(60, callback=lambda *args: None)
        self._api.set_et_stream_control([
            adhawkapi.EyeTrackingStreamTypes.GAZE,
        ], True, callback=lambda *args: None)

        self._api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=lambda *args: None)
        self._api.set_event_control(adhawkapi.EventControlBit.EYE_CLOSE_OPEN, 1, callback=lambda *args: None)

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

    frontend = FrontendData()
    cap = cv2.VideoCapture(1)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if not np.isnan(gaze[0]):
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
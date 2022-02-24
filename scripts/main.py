from gui import XRFWindow
from analysis import XRFAnalyzer
from whoi_nlu_server_messages.StringMessage import StringMessage

import zmq

SHORE_SERVER_URI = "tcp://shore.nui.nolink.io:7776"

def send_pcl_msg(self, msg):
    header = populate_header(msg)

    zmq_msg = PointCloud2Message(
        header,
        msg.height,
        msg.width,
        msg.is_bigendian,
        msg.point_step,
        msg.row_step,
        msg.data,
        msg.is_dense
    )

    try:
        zmq_msg_raw = zmq_msg.to_bytes()
        self.data_socket.send_multipart([self.pcl_topic_zmq, zmq_msg_raw])
        self._unsent_pcl = False
    except BaseException as e:
        print(f"Failed to send pcl message: {e}")

if __name__=="__main__":
    window = XRFWindow()
    analyzer = XRFAnalyzer()

    print(f"Connecting to '{SHORE_SERVER_URI}'...")
    # noinspection PyUnresolvedReferences
    context = zmq.Context()
    data_socket: zmq.Socket = context.socket(zmq.PUB)
    data_socket.connect(SHORE_SERVER_URI)
    data_socket.setsockopt(zmq.SNDHWM, 10)
    print(f"Connected to: '{SHORE_SERVER_URI}'")

    while True:
        window.update()
        if window.send_data:
            print("Sending XRF data!")
            analyzer.runAnalysis(window.mca_filename,
                                 window.calib_filename,
                                 window.cfg_filename)
            window.send_data = False










import zmq
from threading import Semaphore

from whoi_nlu_server_messages.GroundedActionMessage import GroundedActionMessage
from whoi_nlu_server_messages.GroundedActionMessage import GroundedActionParamMessage

hostname = "127.0.0.1"
port = "7775"

def send(self, topic: str, data: bytes):
    topic_raw = topic.encode("ascii")
    with self._socket_lock:
        self._socket.send_multipart([topic_raw, data])


def h2slCallback(topic: str, msg: bytes):# -> Tuple[Optional[UserDescriptor], Optional[str], Union[CBorMessage, bytes]]:
    # Possible topics:
    # "h2sl/command_text"
    # "h2sl/camera_ui"
    # "h2sl/pointcloud_ui"
    # "h2sl/arm_ui"

    # Send test message
    topic_out = "h2sl/pointcloud_ui" # TODO: Remove hardcode
    topic_out_raw = topic_out.encode("ascii")

    # msg = GroundedActionParamMessage("named-transform", "1")
    msg = GroundedActionParamMessage("save-view", "")
    # msg = GroundedActionParamMessage("remove-view", "2")
    # msg = GroundedActionMessage("test", param.as_dict())

    print("sending reply!")
    socket.send_multipart([topic_out_raw, msg.to_bytes()])


if __name__ == '__main__':
    context = zmq.Context()
    # socket OUT
    uri = f"tcp://{hostname}:{port}"
    print(f"Connecting to H2SL service at {uri}...")
    # noinspection PyUnresolvedReferences
    socket: zmq.Socket = context.socket(zmq.REP)
    socket.bind(uri)

    # Cap Msg Queue Size
    socket.setsockopt(zmq.SNDHWM, 10)
    print(f"H2SL Test Link now open at {uri}")

    # Main loop
    while True:
        topic_in_raw, msg_in = socket.recv_multipart()
        topic_in = topic_in_raw.decode("ascii")

        h2slCallback(topic_in, msg_in)

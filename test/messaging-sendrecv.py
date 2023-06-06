import argparse
import json
import signal
import time

from sora_sdk import Sora


class MessagingSendrecv:
    def __init__(self, signaling_url, channel_id, client_id, data_channels, metadata):
        self.sora = Sora()
        self.connection = self.sora.create_connection(
            signaling_url=signaling_url,
            role="sendrecv",
            channel_id=channel_id,
            client_id=client_id,
            metadata=metadata,
            data_channels=data_channels,
            data_channel_signaling=True,
        )

        self.data_channels = data_channels
        self.disconnected = False
        self.shutdown = False
        self.sendable_data_channels = set()
        self.connection.on_data_channel = self.on_data_channel
        self.connection.on_message = self.on_message
        self.connection.on_disconnect = self.on_disconnect

    def on_disconnect(self, ec, message):
        self.disconnected = True

    def on_message(self, label, data):
        print(f"メッセージを受信しました: label={label}, data={data}")

    def on_data_channel(self, label):
        for data_channel in self.data_channels:
            if data_channel["label"] != label:
                continue

            if data_channel["direction"] == "sendrecv" or data_channel["direction"] == "sendonly":
                self.sendable_data_channels.add(label)
                break

    def exit_gracefully(self, signal_number, frame):
        print("\nCtrl+Cが押されました。終了します")
        self.connection.disconnect()
        self.shutdown = True

    def run(self):
        # シグナルを登録し、プログラムが終了するときに正常に処理が行われるようにする
        signal.signal(signal.SIGINT, self.exit_gracefully)

        self.connection.connect()

        i = 0
        while not self.shutdown:
            if i % 100 == 0:
                for label in self.sendable_data_channels:
                    data = f"No. {i / 100}".encode("utf-8")
                    print(f"メッセージを送信します: label={label}, data={data}")
                    self.connection.send_data_channel(label, data)

            time.sleep(0.01)
            i += 1

        self.connection.disconnect()

        # 切断が完了するまで待機
        while not self.disconnected:
            time.sleep(0.01)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # 必須引数
    parser.add_argument("--signaling-url", required=True, help="シグナリング URL")
    parser.add_argument("--channel-id", required=True, help="チャネルID")
    parser.add_argument("--data-channels", required=True,
                        help="使用するデータチャネルを JSON で指定する (例: '[{\"label\": \"#spam\", \"direction\": \"sendrecv\"}]')")

    # オプション引数
    parser.add_argument("--client_id", default='',  help="クライアントID")
    parser.add_argument("--metadata", help="メタデータ JSON")
    args = parser.parse_args()

    metadata = None
    if args.metadata:
        metadata = json.loads(args.metadata)

    messaging_sendrecv = MessagingSendrecv(args.signaling_url,
                                           args.channel_id,
                                           args.client_id,
                                           json.loads(args.data_channels),
                                           metadata)
    messaging_sendrecv.run()

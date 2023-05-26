from view.alert import Alert

class AlertController:
    def __init__(self, msg):
        super().__init__()
        self.alert_window = Alert()
        self.msg = msg

        self.alert_window.msg_lbl.setText(msg)
        self.alert_window.ok_btn.clicked.connect(self.close_alert_window)

    def open_alert_window(self):
        self.alert_window.show()

    def close_alert_window(self):
        self.alert_window.close()

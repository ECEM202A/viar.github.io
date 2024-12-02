import WatchKit
import WatchConnectivity
import SwiftUI

class WatchViewModel: NSObject, ObservableObject, WCSessionDelegate {
    @Published var receivedMessage: String = "No data yet"

    override init() {
        super.init()
        if WCSession.isSupported() {
            WCSession.default.delegate = self
            WCSession.default.activate()
        }
    }

    func session(_ session: WCSession, didReceiveMessage message: [String: Any]) {
        if let data = message["data"] as? String {
            DispatchQueue.main.async {
                self.receivedMessage = data
                WKInterfaceDevice.current().play(.notification) // Haptic feedback
                print("Data received on Watch: \(data)")
            }
        }
    }

    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
        if let error = error {
            print("WCSession activation failed: \(error.localizedDescription)")
        }
    }
}

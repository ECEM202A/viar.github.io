import WatchKit
import WatchConnectivity
import SwiftUI

class WatchViewModel: NSObject, ObservableObject, WCSessionDelegate {
    @Published var receivedMessage: String = "No data yet"

    private var lastMagnitude: Float?

    override init() {
        super.init()
        if WCSession.isSupported() {
            WCSession.default.delegate = self
            WCSession.default.activate()
            print("WCSession activated on Watch.")
        } else {
            print("WCSession is not supported on this device.")
        }
    }

    func session(_ session: WCSession, didReceiveMessage message: [String: Any]) {
        if let data = message["data"] as? String {
            DispatchQueue.main.async {
                self.receivedMessage = data
                self.handleMessage(data)
            }
        } else {
            print("No valid data received on Watch.")
        }
    }

    private func handleMessage(_ data: String) {
        if let magnitude = Float(data) {
            // If the data is a magnitude
            lastMagnitude = magnitude
            adjustHaptics(magnitude: magnitude)
        } else {
            // If the data is a direction or other string, no haptic feedback
            print("Received non-magnitude data: \(data)")
        }
    }

    private func adjustHaptics(magnitude: Float) {
        guard magnitude <= 1.5 else {
            print("No haptic feedback: Magnitude is greater than 1")
            return
        }

        let normalizedMagnitude = 1.5 - magnitude
        print("Adjusting haptics for normalized magnitude: \(normalizedMagnitude)")

        // Simulate stronger haptic feedback with repeated patterns
        if normalizedMagnitude > 1.0 {
            WKInterfaceDevice.current().play(.success) // Strong haptic
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                WKInterfaceDevice.current().play(.success)
            }
        } else if normalizedMagnitude > 0.5 {
            WKInterfaceDevice.current().play(.notification) // Medium haptic
        } else {
            WKInterfaceDevice.current().play(.click) // Weak haptic
        }
    }

    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
        if let error = error {
            print("WCSession activation failed: \(error.localizedDescription)")
        } else {
            print("WCSession activated successfully with state: \(activationState.rawValue)")
        }
    }
}

import Foundation
import Network
import WatchConnectivity

class UDPReceiver: NSObject, ObservableObject, WCSessionDelegate {
    @Published var receivedMessage: String = "No data yet"
    private var listener: NWListener?

    override init() {
        super.init()
        if WCSession.isSupported() {
            WCSession.default.delegate = self
            WCSession.default.activate()
        }
    }

    func startListening() {
        let params = NWParameters.udp
        let port: NWEndpoint.Port = 5005 // Port matching the laptop

        do {
            listener = try NWListener(using: params, on: port)
            listener?.stateUpdateHandler = { state in
                if case .ready = state {
                    print("Listening for UDP on port \(port)")
                }
            }
            listener?.newConnectionHandler = { connection in
                connection.start(queue: .global())
                self.receiveData(on: connection)
            }
            listener?.start(queue: .global())
        } catch {
            print("Failed to start listener: \(error.localizedDescription)")
        }
    }

    private func receiveData(on connection: NWConnection) {
        connection.receiveMessage { data, _, _, error in
            if let data = data, let message = String(data: data, encoding: .utf8) {
                DispatchQueue.main.async {
                    self.receivedMessage = message
                    print("Received from Laptop: \(message)")
                    self.sendToAppleWatch(data: message) // Forward to Watch
                }
            }
            if error == nil {
                self.receiveData(on: connection) // Continue listening
            }
        }
    }

    func sendToAppleWatch(data: String) {
        if WCSession.default.isReachable {
            WCSession.default.sendMessage(["data": data], replyHandler: nil) { error in
                print("Failed to send to watch: \(error.localizedDescription)")
            }
        }
    }

    // WCSessionDelegate required methods
    func sessionDidBecomeInactive(_ session: WCSession) {
        print("Session did become inactive.")
    }

    func sessionDidDeactivate(_ session: WCSession) {
        print("Session did deactivate.")
        WCSession.default.activate()
    }
    
    // WCSessionDelegate methods
    func sessionReachabilityDidChange(_ session: WCSession) {
        print("Session reachability changed: \(session.isReachable)")
    }

    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
        if let error = error {
            print("WCSession activation failed: \(error.localizedDescription)")
        }
    }
}

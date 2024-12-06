import Foundation
import Network
import WatchConnectivity
import AVFoundation

class UDPReceiver: NSObject, ObservableObject, WCSessionDelegate {
    @Published var recentMessages: [String] = [] // Array to show the last messages
    private var listener: NWListener?
    private var directionVotes: [String: Int] = [:] // Tracks votes for directions
    private var audioPlayer: AVAudioPlayer?

    override init() {
        super.init()
        if WCSession.isSupported() {
            WCSession.default.delegate = self
            WCSession.default.activate()
            print("WCSession activated on iPhone.")
        } else {
            print("WCSession is not supported on this device.")
        }

        // Timer to process the majority direction every 3 seconds
        Timer.scheduledTimer(withTimeInterval: 3.0, repeats: true) { _ in
            self.processMajorityDirection()
        }
    }

    func startListening() {
        let params = NWParameters.udp
        let port: NWEndpoint.Port = 53 // Port number to listen on

        do {
            listener = try NWListener(using: params, on: port)
            listener?.stateUpdateHandler = { state in
                switch state {
                case .ready:
                    print("UDP Listener ready on port \(port)")
                case .failed(let error):
                    print("UDP Listener failed: \(error.localizedDescription)")
                default:
                    print("UDP Listener state: \(state)")
                }
            }
            listener?.newConnectionHandler = { connection in
                print("New UDP connection received.")
                connection.start(queue: .global())
                self.receiveData(on: connection)
            }
            listener?.start(queue: .global())
        } catch {
            print("Failed to start UDP Listener: \(error.localizedDescription)")
        }
    }

    private func receiveData(on connection: NWConnection) {
        connection.receiveMessage { data, _, _, error in
            if let error = error {
                print("Error receiving UDP data: \(error.localizedDescription)")
            }

            if let data = data, let message = String(data: data, encoding: .utf8) {
                DispatchQueue.main.async {
                    // Add new message to recent messages
                    self.recentMessages.append(message)
                    if self.recentMessages.count > 10 {
                        self.recentMessages.removeFirst() // Keep only the last 10 messages
                    }

                    // Update voting system
                    self.directionVotes[message, default: 0] += 1

                    // Log message
                    print("Received from Laptop: \(message)")
                    self.sendToAppleWatch(data: message) // Forward to Apple Watch
                }
            }

            if error == nil {
                self.receiveData(on: connection) // Continue listening
            }
        }
    }

    private func processMajorityDirection() {
        // Find the majority direction
        guard !directionVotes.isEmpty else { return }
        let majorityDirection = directionVotes.max(by: { $0.value < $1.value })?.key ?? "wait"

        // Play the audio for the majority direction
        playDirection(direction: majorityDirection)

        // Clear votes for the next interval
        directionVotes.removeAll()
    }

    private func playDirection(direction: String) {
        print("Majority direction: \(direction)")

        // Load the corresponding .mp3 file
        guard let url = Bundle.main.url(forResource: direction, withExtension: "m4a") else {
            print("Audio file for \(direction) not found.")
            return
        }

        do {
            audioPlayer = try AVAudioPlayer(contentsOf: url)
            audioPlayer?.play()
        } catch {
            print("Failed to play audio for \(direction): \(error.localizedDescription)")
        }
    }

    func sendToAppleWatch(data: String) {
        if WCSession.default.isReachable {
            print("Attempting to send message to Apple Watch...")
            WCSession.default.sendMessage(["data": data], replyHandler: nil) { error in
                print("Failed to send to Apple Watch: \(error.localizedDescription)")
            }
            print("Message sent to Apple Watch: \(data)")
        } else {
            print("Apple Watch is not reachable.")
        }
    }

    // WCSessionDelegate required methods
    func sessionDidBecomeInactive(_ session: WCSession) {
        print("WCSession did become inactive.")
    }

    func sessionDidDeactivate(_ session: WCSession) {
        print("WCSession did deactivate.")
        WCSession.default.activate()
    }

    func sessionReachabilityDidChange(_ session: WCSession) {
        print("WCSession reachability changed: \(session.isReachable)")
    }

    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
        if let error = error {
            print("WCSession activation failed: \(error.localizedDescription)")
        } else {
            print("WCSession activated successfully with state: \(activationState.rawValue)")
        }
    }
}

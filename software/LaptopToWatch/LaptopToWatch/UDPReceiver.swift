import Foundation
import Network
import WatchConnectivity
import AVFoundation
import CoreHaptics

class UDPReceiver: NSObject, ObservableObject, WCSessionDelegate {
    @Published var recentMessages: [String] = [] // Array to show the last messages
    private var listener: NWListener?
    private var directionVotes: [String: Int] = [:] // Tracks votes for directions
    private var audioPlayer: AVAudioPlayer?
    private var hapticEngine: CHHapticEngine?
    private var lastReceivedDirection: String? // To store the last received direction
    private var lastReceivedMagnitude: Float? // To store the last received magnitude

    override init() {
        super.init()
        setupHaptics()
        if WCSession.isSupported() {
            WCSession.default.delegate = self
            WCSession.default.activate()
            print("WCSession activated on iPhone.")
        } else {
            print("WCSession is not supported on this device.")
        }

        // Timer to process the majority direction every 0.5 seconds
        Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { _ in
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
                    self.recentMessages.append(message)
                    if self.recentMessages.count > 10 {
                        self.recentMessages.removeFirst() // Keep only the last 10 messages
                    }

                    print("Received from Laptop: \(message)")
                    self.handleMessage(message)
                }
            }

            if error == nil {
                self.receiveData(on: connection) // Continue listening
            }
        }
    }

    private func handleMessage(_ message: String) {
        if let floatMagnitude = Float(message) {
            self.lastReceivedMagnitude = floatMagnitude
            self.adjustHaptics(magnitude: floatMagnitude)

            // Send magnitude to Apple Watch
            sendToAppleWatch(data: message)
        } else {
            self.lastReceivedDirection = message
            directionVotes[message, default: 0] += 1

            // Send direction to Apple Watch
            sendToAppleWatch(data: message)
        }
    }

    private func processMajorityDirection() {
        guard !directionVotes.isEmpty else { return }
        let majorityDirection = directionVotes.max(by: { $0.value < $1.value })?.key ?? "wait"
        playDirection(direction: majorityDirection)
        directionVotes.removeAll()
    }

    private func playDirection(direction: String) {
        print("Majority direction: \(direction)")

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

    private func adjustHaptics(magnitude: Float) {
        guard magnitude <= 1.0 else { return }

        let normalizedMagnitude = 1.0 - magnitude
        let hapticStrength = max(0.0, min(1.0, normalizedMagnitude))

        do {
            let pattern = try CHHapticPattern(events: [
                CHHapticEvent(eventType: .hapticContinuous,
                              parameters: [CHHapticEventParameter(parameterID: .hapticIntensity, value: hapticStrength)],
                              relativeTime: 0,
                              duration: 0.2)
            ], parameters: [])

            let player = try hapticEngine?.makePlayer(with: pattern)
            try player?.start(atTime: 0)
            print("Haptic feedback triggered with strength: \(hapticStrength)")
        } catch {
            print("Failed to trigger haptic feedback: \(error.localizedDescription)")
        }
    }

    private func setupHaptics() {
        guard CHHapticEngine.capabilitiesForHardware().supportsHaptics else {
            print("Haptics not supported on this device.")
            return
        }

        do {
            hapticEngine = try CHHapticEngine()
            try hapticEngine?.start()
        } catch {
            print("Failed to start haptic engine: \(error.localizedDescription)")
        }
    }

    func sendToAppleWatch(data: String) {
        guard WCSession.default.isReachable else {
            print("Apple Watch is not reachable.")
            return
        }

        WCSession.default.sendMessage(["data": data], replyHandler: nil) { error in
            print("Failed to send data to Apple Watch: \(error.localizedDescription)")
        }
        print("Message sent to Apple Watch: \(data)")
    }

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

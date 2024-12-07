import Foundation
import Speech
import AVFoundation
import Network

class SpeechRecognitionManager: NSObject, ObservableObject, SFSpeechRecognizerDelegate {
    @Published var isRecording: Bool = false
    @Published var recognizedText: String = ""
    
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))!
    private var recognitionTask: SFSpeechRecognitionTask?
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private let audioEngine = AVAudioEngine()
    
    // UDP connection properties
    private var connection: NWConnection?
    private let host = "131.179.73.228" // Replace with your laptop's IP
    private let port: UInt16 = 5005    // Replace with the desired port
    
    override init() {
        super.init()
        speechRecognizer.delegate = self
        requestPermissions()
        
        // Initialize the UDP connection
        connection = NWConnection(
            host: NWEndpoint.Host(host),
            port: NWEndpoint.Port(integerLiteral: port),
            using: .udp
        )
        connection?.start(queue: .global())
    }
    
    func requestPermissions() {
        // Request microphone permissions
        AVAudioSession.sharedInstance().requestRecordPermission { granted in
            DispatchQueue.main.async {
                if granted {
                    print("Microphone permission granted.")
                } else {
                    print("Microphone permission denied.")
                }
            }
        }
        
        // Request speech recognition permissions
        SFSpeechRecognizer.requestAuthorization { authStatus in
            DispatchQueue.main.async {
                switch authStatus {
                case .authorized:
                    print("Speech recognition permission granted.")
                case .denied:
                    print("Speech recognition permission denied.")
                case .restricted:
                    print("Speech recognition permission restricted.")
                case .notDetermined:
                    print("Speech recognition permission not determined.")
                @unknown default:
                    fatalError("Unhandled authorization status.")
                }
            }
        }
    }
    
    func startRecording() {
        guard !audioEngine.isRunning else {
            stopRecording()
            return
        }
        
        isRecording = true
        recognizedText = ""
        
        // Cancel any existing recognition tasks
        recognitionTask?.cancel()
        recognitionTask = nil
        
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(.record, mode: .measurement, options: .duckOthers)
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        } catch {
            print("Audio session configuration error: \(error.localizedDescription)")
            return
        }
        
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else { return }
        recognitionRequest.shouldReportPartialResults = true
        recognitionRequest.requiresOnDeviceRecognition = true // Enable on-device recognition if needed
        
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
            self.recognitionRequest?.append(buffer)
        }
        
        audioEngine.prepare()
        do {
            try audioEngine.start()
        } catch {
            print("Audio engine start error: \(error.localizedDescription)")
            return
        }
        
        recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { result, error in
            if let result = result {
                DispatchQueue.main.async {
                    self.recognizedText = result.bestTranscription.formattedString
                }
                
                // Check for specific keywords and send them via UDP
                let recognizedText = result.bestTranscription.formattedString.lowercased()
                if recognizedText.contains("bottle") {
                    self.sendMessage("bottle")
                } else if recognizedText.contains("laptop") {
                    self.sendMessage("laptop")
                }
            }
            
            if let error = error {
                print("Speech recognition task error: \(error.localizedDescription)")
                self.stopRecording()
            }
        }
    }
    
    func stopRecording() {
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        recognitionRequest?.endAudio()
        isRecording = false
        
        // Reset the audio session to allow playback after stopping recording
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(.playback, mode: .default)
            try audioSession.setActive(true)
        } catch {
            print("Error resetting audio session: \(error.localizedDescription)")
        }
    }
    
    private func sendMessage(_ message: String) {
        guard let messageData = message.data(using: .utf8) else { return }
        connection?.send(content: messageData, completion: .contentProcessed { error in
            if let error = error {
                print("Failed to send message: \(error.localizedDescription)")
            } else {
                print("Message sent: \(message)")
            }
        })
    }
    
    func speechRecognizer(_ speechRecognizer: SFSpeechRecognizer, availabilityDidChange available: Bool) {
        DispatchQueue.main.async {
            self.isRecording = false
        }
    }
}

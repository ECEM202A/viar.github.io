/*
See the LICENSE.txt file for this sample’s licensing information.

Abstract:
The root view controller that provides a button to start and stop recording, and which displays the speech recognition results.
*/

import UIKit
import Speech
import Foundation
import AVKit
import Network

public class ViewController: UIViewController, SFSpeechRecognizerDelegate {
    // MARK: Properties
    private var audioFile = "test_song"
        
    private var player: AVAudioPlayer?
    private var isplaying = false
    private var totalTime: TimeInterval = 0.0
    private var currentTime: TimeInterval = 0.0
    private var soundPlaying = false
    
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))!
    
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    
    private var recognitionTask: SFSpeechRecognitionTask?
    
    private let audioEngine = AVAudioEngine()
    
    @IBOutlet var textView: UITextView!
    
    @IBOutlet var recordButton: UIButton!
    
    // Create a UDP connection to the laptop
    var connection: NWConnection?
    
    // MARK: Custom LM Support

    @available(iOS 17, *)
    private var lmConfiguration: SFSpeechLanguageModel.Configuration {
        let outputDir = FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask).first!
        let dynamicLanguageModel = outputDir.appendingPathComponent("LM")
        let dynamicVocabulary = outputDir.appendingPathComponent("Vocab")
        return SFSpeechLanguageModel.Configuration(languageModel: dynamicLanguageModel, vocabulary: dynamicVocabulary)
    }
    
    // MARK: UIViewController
    
    public override func viewDidLoad() {
        super.viewDidLoad()
        self.setupAudio()
        // Disable the record buttons until authorization has been granted.
        recordButton.isEnabled = false
        // Replace with your laptop's IP address and port
        let laptopIPAddress = "192.168.1.82" // Replace with your laptop's IP
        let port: UInt16 = 5000              // Replace with the desired port

        // Initialize the UDP connection
        connection = NWConnection(host: NWEndpoint.Host(laptopIPAddress), port: NWEndpoint.Port(integerLiteral: port), using: .udp)
        connection?.start(queue: .global())
    }
    
    override public func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        // Configure the SFSpeechRecognizer object already
        // stored in a local member variable.
        speechRecognizer.delegate = self
        
        // Make the authorization request.
        SFSpeechRecognizer.requestAuthorization { authStatus in

            // Divert to the app's main thread so that the UI
            // can be updated.
            OperationQueue.main.addOperation {
                switch authStatus {
                case .authorized:
                    if #available(iOS 17, *) {
                        Task.detached {
                            do {
                                let assetPath = Bundle.main.path(forResource: "CustomLMData", ofType: "bin", inDirectory: "customlm/en_US")!
                                let assetUrl = URL(fileURLWithPath: assetPath)
                                try await SFSpeechLanguageModel.prepareCustomLanguageModel(for: assetUrl,
                                                                                           clientIdentifier: "com.apple.SpokenWord",
                                                                                           configuration: self.lmConfiguration)
                            } catch {
                                NSLog("Failed to prepare custom LM: \(error.localizedDescription)")
                            }
                            await MainActor.run { self.recordButton.isEnabled = true }
                        }
                    } else {
                        self.recordButton.isEnabled = true
                    }
                case .denied:
                    self.recordButton.isEnabled = false
                    self.recordButton.setTitle("User denied access to speech recognition", for: .disabled)
                    
                case .restricted:
                    self.recordButton.isEnabled = false
                    self.recordButton.setTitle("Speech recognition restricted on this device", for: .disabled)
                    
                case .notDetermined:
                    self.recordButton.isEnabled = false
                    self.recordButton.setTitle("Speech recognition not yet authorized", for: .disabled)
                    
                default:
                    self.recordButton.isEnabled = false
                }
            }
        }
    }
    
    private func startRecording() throws {
        
        // Cancel the previous task if it's running.
        if let recognitionTask = recognitionTask {
            recognitionTask.cancel()
            self.recognitionTask = nil
        }
        
        // Configure the audio session for the app.
        let audioSession = AVAudioSession.sharedInstance()
        try audioSession.setCategory(.playAndRecord, mode: .measurement, options: .duckOthers)
        try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        let inputNode = audioEngine.inputNode

        // Create and configure the speech recognition request.
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else { fatalError("Unable to created a SFSpeechAudioBufferRecognitionRequest object") }
        recognitionRequest.shouldReportPartialResults = true
        
        // Keep speech recognition data on device
        if #available(iOS 13, *) {
            recognitionRequest.requiresOnDeviceRecognition = true
            if #available(iOS 17, *) {
                recognitionRequest.customizedLanguageModel = self.lmConfiguration
            }
        }
        
        // Create a recognition task for the speech recognition session.
        // Keep a reference to the task so that it can be canceled.
        recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { result, error in
            var isFinal = false
            
            if let result = result {
                // Update the text view with the results.
                let recognized_text = result.bestTranscription.formattedString
                if recognized_text.contains("keys") {
                    self.textView.text = "keys keyword found"
                    self.sendMessage()
                    self.playAudio()
                } else {
                    self.textView.text = "No keyword found"
                    self.stopAudio()
                }
//                self.textView.text = result.bestTranscription.formattedString
                
                isFinal = result.isFinal
            }
            
            if error != nil || isFinal {
                // Stop recognizing speech if there is a problem.
                self.audioEngine.stop()
                inputNode.removeTap(onBus: 0)
                
                self.recognitionRequest = nil
                self.recognitionTask = nil
                
                self.recordButton.isEnabled = true
                self.recordButton.setTitle("Start Recording", for: [])
            }
        }

        // Configure the microphone input.
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { (buffer: AVAudioPCMBuffer, when: AVAudioTime) in
            self.recognitionRequest?.append(buffer)
        }
        
        audioEngine.prepare()
        try audioEngine.start()
        
        // Let the user know to start talking.
        textView.text = "(Go ahead, I'm listening)"
    }
    
    // MARK: SFSpeechRecognizerDelegate
    
    public func speechRecognizer(_ speechRecognizer: SFSpeechRecognizer, availabilityDidChange available: Bool) {
        if available {
            recordButton.isEnabled = true
            recordButton.setTitle("Start Recording", for: [])
        } else {
            recordButton.isEnabled = false
            recordButton.setTitle("Recognition Not Available", for: .disabled)
        }
    }
    
    // MARK: Interface Builder actions

    @IBAction func playSound(_ sender: Any) {
        if soundPlaying {
            stopAudio()
        } else {
            setupAudio()
        }
    }
    
    @IBAction func recordButtonTapped() {
        
        if audioEngine.isRunning {
            audioEngine.stop()
            recognitionRequest?.endAudio()
            recordButton.isEnabled = false
//            setupAudio()
//            sleep(10)
            recordButton.setTitle("Stopping", for: .disabled)
        } else {
            do {
                try startRecording()
                recordButton.setTitle("Stop Recording", for: [])
            } catch {
                recordButton.setTitle("Recording Not Available", for: [])
            }
        }
    }
    
    public func setupAudio() {
                guard let url = Bundle.main.url(forResource: audioFile, withExtension: "mp3") else { return }
            let audiofile = try! AVAudioFile(forReading: url)
    //        let playernode = AVAudioPlayerNode()
    //        audioEngine.attach(playernode)
    //        audioEngine.connect(playernode,
    //                            to: audioEngine.outputNode,
    //                            format: audiofile.processingFormat)
    //        playernode.scheduleFile(audiofile,
    //                                at: nil,
    //                                completionCallbackType: .dataPlayedBack) { _ in
    //            /* Handle any work that's necessary after playback. */
    //        }
    //        do {
    //            try audioEngine.start()
    //            playernode.play()
    //        } catch {
    //            /* Handle the error. */
    //        }
                do {
                    print("trying audio")
                    player = try AVAudioPlayer(contentsOf: url)
                    player?.prepareToPlay()
                   totalTime = player?.duration ?? 0.0
//                    playAudio()
                } catch {
                    print("Error loading audio: \(error)")
                }
            }
        
        public func playAudio() {
            player?.play()
            soundPlaying = true
            }
        public func stopAudio() {
            player?.stop()
            soundPlaying = false
            }
func sendMessage() {
        // Message to send
        let message = "Hello from iPhone!"
        if let messageData = message.data(using: .utf8) {
            connection?.send(content: messageData, completion: .contentProcessed({ error in
                if let error = error {
                    print("Failed to send message: \(error)")
                } else {
                    print("Message sent successfully!")
                }
            }))
        }
    }
}


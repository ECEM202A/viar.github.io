import SwiftUI

struct ContentView: View {
    @StateObject private var receiver = UDPReceiver()
    @StateObject private var speechManager = SpeechRecognitionManager()

    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                Text("UDP to Watch App")
                    .font(.headline)

                Text("Received Messages:")
                    .font(.subheadline)

                ForEach(receiver.recentMessages.reversed(), id: \.self) { message in
                    Text(message)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(10)
                }

                Text("Speech Recognition:")
                    .font(.subheadline)

                Text(speechManager.recognizedText)
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color.blue.opacity(0.2))
                    .cornerRadius(10)

                Button(action: {
                    do {
                        try speechManager.startRecording()
                    } catch {
                        print("Error starting speech recognition: \(error)")
                    }
                }) {
                    Text("Start Speech Recognition")
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }

                Button(action: {
                    speechManager.stopRecording()
                }) {
                    Text("Stop Speech Recognition")
                        .padding()
                        .background(Color.red)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }

                Spacer()
            }
            .padding()
        }
        .onAppear {
            receiver.startListening()
        }
    }
}

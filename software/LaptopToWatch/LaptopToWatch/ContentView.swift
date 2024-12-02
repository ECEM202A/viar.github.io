import SwiftUI

struct ContentView: View {
    @StateObject private var receiver = UDPReceiver()
    var body: some View {
        VStack(spacing: 20) {
            Text("UDP to Watch App")
                .font(.headline)

            Text("Received from Laptop:")
                .font(.subheadline)
            Text(receiver.receivedMessage)
                .padding()
                .frame(maxWidth: .infinity)
                .background(Color.gray.opacity(0.2))
                .cornerRadius(10)

            Spacer()
        }
        .padding()
        .onAppear {
            receiver.startListening()
        }
    }
}

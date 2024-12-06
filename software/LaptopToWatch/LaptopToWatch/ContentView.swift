import SwiftUI

struct ContentView: View {
    @StateObject private var receiver = UDPReceiver()
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

                Spacer()
            }
            .padding()
        }
        .onAppear {
            receiver.startListening()
        }
    }
}

import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = WatchViewModel()

    var body: some View {
        ScrollView { // Add a ScrollView
            VStack(spacing: 20) {
                Text("Data from iPhone:")
                    .font(.headline)

                Text(viewModel.receivedMessage)
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color.gray.opacity(0.2))
                    .cornerRadius(10)

                Spacer()
            }
            .padding()
        }
    }
}

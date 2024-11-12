import SwiftUI
import WatchKit

struct ContentView: View {
    @State private var hapticTimer: Timer?
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                Text("Haptic Feedback Demo")
                    .font(.headline)
                    .padding(.top)
                
                // Slow Frequency Haptic
                Button(action: {
                    startHapticFeedback(type: .click, interval: 1.0) // 1 second interval
                }) {
                    Text("Click Haptic (Slow)")
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                
                // Medium Frequency Haptic
                Button(action: {
                    startHapticFeedback(type: .directionUp, interval: 0.5) // 0.5 second interval
                }) {
                    Text("Direction Up Haptic (Medium)")
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                
                // Fast Frequency Haptic
                Button(action: {
                    startHapticFeedback(type: .retry, interval: 0.25) // 0.25 second interval
                }) {
                    Text("Direction Down Haptic (Fast)")
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.orange)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                
                // Very Fast Frequency Haptic
                Button(action: {
                    startHapticFeedback(type: .notification, interval: 0.1) // 0.1 second interval
                }) {
                    Text("Success Haptic (Very Fast)")
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.purple)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                
                // Stop Button
                Button(action: {
                    stopHapticFeedback()
                }) {
                    Text("Stop Haptic Feedback")
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.red)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
            }
            .padding()
        }
    }
    
    func startHapticFeedback(type: WKHapticType, interval: TimeInterval) {
        // Stop any existing timer
        hapticTimer?.invalidate()
        
        // Start a new timer with the specified interval
        hapticTimer = Timer.scheduledTimer(withTimeInterval: interval, repeats: true) { _ in
            WKInterfaceDevice.current().play(type)
        }
    }
    
    func stopHapticFeedback() {
        // Invalidate the timer to stop haptic feedback
        hapticTimer?.invalidate()
        hapticTimer = nil
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

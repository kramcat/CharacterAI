//
//  GuidanceViewModel.swift
//  ai_parent
//
//  Created by Adolfo Calderon on 11/10/23.
//
import Combine
import SwiftUI


class GuidanceViewModel: ObservableObject {
    @Published var displayedText = ""
    @Published var isTyping = false
    @Published var isWaitingForResponse = false
    @Published var userInput: String = ""

    private var model = GuidanceModel()
    private var fullResponse: String = ""
    private var typingTimer: Timer?
    private var currentIndex = 0
    
// When the user submits a prompt, we start waiting for the response.
    func submitPrompt() {
        self.isWaitingForResponse = true
        model.prompt = userInput
        
        // Call the model to submit the prompt.
        model.submitPrompt { [weak self] result in
            // When the result comes back, we are no longer waiting.
            DispatchQueue.main.async {
                self?.isWaitingForResponse = false
                switch result {
                case .success(let response):
                    // If success, start the typing effect with the response.
                    self?.prepareTypingEffect(with: response)
                case .failure(let error):
                    // If failure, show the error message.
                    self?.displayedText = "Error: \(error.localizedDescription)"
                    self?.isTyping = false
                }
            }
        }
    }
    
    // Prepare for typing effect by setting up initial state.
    private func prepareTypingEffect(with response: String) {
        fullResponse = response
        currentIndex = 0
        displayedText = ""
        isTyping = true
        startTypingEffect()
    }
    
    // Start the timer that simulates typing effect.
    private func startTypingEffect() {
        typingTimer?.invalidate()
        
        typingTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] timer in
            DispatchQueue.main.async {
                self?.typeNextCharacter()
            }
        }
    }
    
    // Append the next character of the response to the displayed text.
    private func typeNextCharacter() {
        if currentIndex < fullResponse.count {
            let index = fullResponse.index(fullResponse.startIndex, offsetBy: currentIndex)
            displayedText.append(fullResponse[index])
            currentIndex += 1
        } else {
            // Once the end is reached, stop typing and invalidate the timer.
            isTyping = false
            typingTimer?.invalidate()
        }
    }
    
    // Invalidate the timer when the ViewModel deinitializes.
    deinit {
        typingTimer?.invalidate()
    }
}

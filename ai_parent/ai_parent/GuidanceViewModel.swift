//
//  GuidanceViewModel.swift
//  ai_parent
//
//  Created by Adolfo Calderon on 11/10/23.
//
import Combine
import SwiftUI

class GuidanceViewModel: ObservableObject {
    // Private model
    private var model = GuidanceModel()

    // Public facing prompt that the View can bind to
    @Published var userInput: String = ""
    
    // Method to call when the prompt needs to be submitted
    func submitPrompt() {
        model.prompt = userInput
        model.submitPrompt { result in
            switch result {
            case .success(let response):
                // Update any Published properties with the result as needed
                print(response)
            case .failure(let error):
                // Handle the error, update the View with an error message if needed
                print(error.localizedDescription)
            }
        }
    }
}

//
//  GuidanceHomeView.swift
//  ai_parent
//
//  Created by Adolfo Calderon on 11/10/23.
//

import SwiftUI

struct GuidanceHomeView: View {
    @StateObject private var viewModel = GuidanceViewModel()

    var body: some View {
        ZStack {
//            Image("dunks").resizable().edgesIgnoringSafeArea(/*@START_MENU_TOKEN@*/.all/*@END_MENU_TOKEN@*/)
            Color.white.opacity(0.1).edgesIgnoringSafeArea(.all)
            VStack {
                title
                apiResponse
                prompt
                promptButton
            }
        }
    }
    
    var title: some View {
        Group {
            Spacer()
            Text("Guidance AI")
                .font(.largeTitle) // Large and easy to read
                .fontWeight(.bold) // Make it bold
                .foregroundColor(Color.green.opacity(0.65)) // Warm color for the text
                .padding(.bottom, 50) // Space from the bottom
            Spacer()
        }

    }
    
    var prompt: some View {
        TextField("Ask me anything...", text: $viewModel.userInput)
            .textFieldStyle(RoundedBorderTextFieldStyle())
            .padding() // Padding around the TextField
            .font(Font.system(size: 18, design: .rounded)) // Rounded, easy-on-the-eyes font
            .foregroundColor(Color.brown) // Warm color for the input text
            .background(Color.white) // White background for the TextField
            .cornerRadius(10) // Rounded corners for the TextField background
            .padding(.horizontal, 20) // Horizontal padding for the TextField
        
    }
    
    var promptButton: some View {
        Button(action: {
            viewModel.submitPrompt()
        }) {
            Image(systemName: "arrow.right.circle.fill")
                .font(.largeTitle) // Size of the SF Symbol
                .foregroundColor(Color.green.opacity(0.65)) // Warm color for the icon
        }
        .padding(.bottom, 20) // Push the button up a little from the bottom edge
    }
    
    
    var apiResponse: some View {
        Group {
            Spacer()
            if viewModel.isWaitingForResponse {
                showLoadingIcon
            } else {
                showResponse
            }
            Spacer()
        }
    }
    
    var showLoadingIcon: some View {
        // Show a progress view while waiting for the server response.
        ProgressView()
            .progressViewStyle(CircularProgressViewStyle(tint: .green))
            .scaleEffect(1.5)
    }
    
    var showResponse: some View {
        // Display the text that has been "typed" out.
        Text(viewModel.displayedText)
            .padding()
            .transition(.opacity) // Fade in/out the text as it appears/disappears
    }
}

#Preview {
    GuidanceHomeView()
}


// Need to implement conversation persistance?
// Do I need to pass data back into the api to maintain the conversation? What happens to previous conversation resopnses?
    // How does the engine work off of previous convos is the question

// I think the backend stores the responses
// The frontend would just send another prompts out, for another response from the engine

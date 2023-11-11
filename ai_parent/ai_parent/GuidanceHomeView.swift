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
            Color.orange.opacity(0.1).edgesIgnoringSafeArea(.all)
            VStack {
                title
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
                .foregroundColor(Color.orange) // Warm color for the text
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
                .foregroundColor(Color.orange) // Warm color for the icon
        }
        .padding(.bottom, 20) // Push the button up a little from the bottom edge
    }
}

#Preview {
    GuidanceHomeView()
}

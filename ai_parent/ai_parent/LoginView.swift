//
//  LoginView.swift
//  ai_parent
//
//  Created by Adolfo Calderon on 11/11/23.
//

import SwiftUI

struct LoginView: View {
    @StateObject private var loginViewModel = LoginViewModel()

    var body: some View {
        ZStack {
            Color.white.opacity(0.1).edgesIgnoringSafeArea(.all)
            VStack {
                title
                userNameInput
                passwordInput
                loginButton
            }
            .padding()
            // This part checks if the user is authenticated and shows the main view.
            .fullScreenCover(isPresented: $loginViewModel.isAuthenticated) {
                GuidanceHomeView()
            }
        }

    }
    var title: some View {
        Text("Login")
            .font(.largeTitle)
            .fontWeight(.bold)
            .padding()
    }
    
    var userNameInput: some View {
        TextField("Username", text: $loginViewModel.username)
            .textFieldStyle(RoundedBorderTextFieldStyle())
            .overlay(
                RoundedRectangle(cornerRadius: 8) // This Rounded Rectangle will act as the border
                    .stroke(Color.primary, lineWidth: 0.1)
                    )
            .padding()
    }
    
    var passwordInput: some View {
        SecureField("Password", text: $loginViewModel.password)
            .textFieldStyle(RoundedBorderTextFieldStyle())
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color.primary, lineWidth: 0.1)
                    )
            .padding()
    }
    var loginButton: some View {
        Button(action: loginViewModel.login) {
            Text("Sign In")
                .foregroundColor(.white)
                .frame(minWidth: 0, maxWidth: .infinity)
                .padding()
                .background(Color.green.opacity(0.65))
                .cornerRadius(10)
        }
        .disabled(!loginViewModel.isFormValid)
    }
    
}

#Preview {
    LoginView()
}

//
//  LoginViewModel.swift
//  ai_parent
//
//  Created by Adolfo Calderon on 11/11/23.
//

import SwiftUI

class LoginViewModel: ObservableObject {
    @Published var username: String = ""
    @Published var password: String = ""
    @Published var isAuthenticated: Bool = false

    var isFormValid: Bool {
            !username.isEmpty && !password.isEmpty
        }
    
    func login() {
        // Perform login logic...
        isAuthenticated = isFormValid
    }
}

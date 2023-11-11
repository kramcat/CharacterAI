//
//  GuidanceModel.swift
//  ai_parent
//
//  Created by Adolfo Calderon on 11/10/23.
//

import Foundation

struct GuidanceModel {
    var prompt: String = ""
    
    // This function would be used to interact with an API
    func submitPrompt(completion: @escaping (Result<String, Error>) -> Void) {
        // API call would be made here
    }
}

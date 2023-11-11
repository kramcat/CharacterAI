//
//  ai_parentApp.swift
//  ai_parent
//
//  Created by Adolfo Calderon on 11/10/23.
//

import SwiftUI

@main
struct ai_parentApp: App {
//    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            LoginView()
//            ContentView()
//                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}

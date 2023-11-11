import Foundation
import Alamofire  // If using Alamofire

class DIDTextToVideoService {
    static let shared = DIDTextToVideoService()

    private let apiKey = "a2lsbGFzaG90MDA3QGdtYWlsLmNvbQ:Sw0OeFJloojCJDJ54YiZy"
    private let apiURL = "https://api.did.com/text-to-video"

    func createVideo(from text: String, completion: @escaping (Result<String, Error>) -> Void) {
        let headers: HTTPHeaders = [
            "Authorization": "Bearer \(apiKey)",
            "Content-Type": "application/json"
        ]

        let parameters: [String: Any] = ["text": text]

        AF.request(apiURL, method: .post, parameters: parameters, encoding: JSONEncoding.default, headers: headers)
            .responseJSON { response in
                switch response.result {
                case .success:
                    if let data = response.data, let videoURL = String(data: data, encoding: .utf8) {
                        completion(.success(videoURL))
                    } else {
                        completion(.failure(NSError(domain: "ParsingError", code: 1, userInfo: nil)))
                    }
                case .failure(let error):
                    completion(.failure(error))
                }
            }
    }
}

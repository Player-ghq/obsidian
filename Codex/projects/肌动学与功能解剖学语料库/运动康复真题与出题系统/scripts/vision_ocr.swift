import Foundation
import Vision
import AppKit

func usage() -> Never {
    fputs("usage: vision_ocr <image-path> [output-path]\n", stderr)
    exit(2)
}

guard CommandLine.arguments.count >= 2 else { usage() }

let imagePath = CommandLine.arguments[1]
let outputPath = CommandLine.arguments.count >= 3 ? CommandLine.arguments[2] : nil
let url = URL(fileURLWithPath: imagePath)

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true
if let supported = try? request.supportedRecognitionLanguages(),
   supported.contains("zh-Hans") {
    request.recognitionLanguages = ["zh-Hans", "en-US"].filter { supported.contains($0) }
}
request.minimumTextHeight = 0.008

let handler = VNImageRequestHandler(url: url, options: [:])

do {
    try handler.perform([request])
} catch {
    fputs("OCR failed: \(error)\n", stderr)
    exit(1)
}

let observations = request.results ?? []
let lines = observations.compactMap { obs -> String? in
    guard let candidate = obs.topCandidates(1).first else { return nil }
    let text = candidate.string.trimmingCharacters(in: .whitespacesAndNewlines)
    return text.isEmpty ? nil : text
}

let output = lines.joined(separator: "\n")
if let outputPath {
    try output.write(toFile: outputPath, atomically: true, encoding: .utf8)
} else {
    print(output)
}

/*
See the LICENSE.txt file for this sample’s licensing information.

Abstract:
A simple utility for generating Custom LM training data
*/

import Speech
print("trying")
let data = SFCustomLanguageModelData(locale: Locale(identifier: "en_US"), identifier: "com.apple.SpokenWord", version: "1.0") {
    
    SFCustomLanguageModelData.PhraseCount(phrase: "Play the Albin counter gambit", count: 10)
    
    // Find Commands
    SFCustomLanguageModelData.PhraseCountsFromTemplates(classes: [
//        "piece": ["pawn", "rook", "knight", "bishop", "queen", "king"],
//        "royal": ["queen", "king"],
        "object": ["phone", "laptop", "remote", "keys", "cup", "cane", "glasses"]
//        "rank": Array(1...8).map({ String($0) })
    ]) {
        SFCustomLanguageModelData.TemplatePhraseCountGenerator.Template(
            "Find my <object>",
            count: 10_000
        )
    }

//    SFCustomLanguageModelData.CustomPronunciation(grapheme: "Winawer", phonemes: ["w I n aU @r"])
//    SFCustomLanguageModelData.CustomPronunciation(grapheme: "Tartakower", phonemes: ["t A r t @ k aU @r"])

//    SFCustomLanguageModelData.PhraseCount(phrase: "Play the Winawer variation", count: 10)
//    SFCustomLanguageModelData.PhraseCount(phrase: "Play the Tartakower", count: 10)
}
let path = FileManager.default.currentDirectoryPath
try await data.export(to: URL(filePath: path + "/../SpokenWord/customlm/en_US/customLMDataVIAR.bin"))
print("done")


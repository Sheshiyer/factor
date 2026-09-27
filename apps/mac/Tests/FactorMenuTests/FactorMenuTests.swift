import Foundation
import XCTest
@testable import FactorMenu

final class FactorMenuTests: XCTestCase {
    private func fixture() throws -> URL {
        let root = FileManager.default.temporaryDirectory.resolvingSymlinksInPath()
            .appendingPathComponent("FactorMenuTests-\(UUID().uuidString)")
        try FileManager.default.createDirectory(at: root, withIntermediateDirectories: false)
        addTeardownBlock { try FileManager.default.removeItem(at: root) }
        return root
    }

    func testSessionThenMissingCompanyPreferenceDefaultsEnglish() async throws {
        let root = try fixture()
        await MainActor.run {
            let manager = LanguageManager()
            XCTAssertNil(manager.setLanguage(.fr, companyPath: nil))
            XCTAssertEqual(manager.current, .fr)
            XCTAssertNil(manager.load(companyPath: root.path))
            XCTAssertEqual(manager.current, .en)
            XCTAssertFalse(FileManager.default.fileExists(atPath: root.appendingPathComponent("preferences.json").path))
        }
    }

    func testFreshAndExistingAtomicWritesPreserveKeys() async throws {
        let root = try fixture()
        try await MainActor.run {
            let manager = LanguageManager()
            XCTAssertNil(manager.setLanguage(.fr, companyPath: root.path))
            let file = root.appendingPathComponent("preferences.json")
            XCTAssertEqual(try JSONSerialization.jsonObject(with: Data(contentsOf: file)) as? [String: String], ["language": "fr"])
            try Data(#"{"theme":{"dark":true},"count":3}"#.utf8).write(to: file)
            XCTAssertNil(manager.load(companyPath: root.path))
            XCTAssertEqual(manager.current, .en)
            XCTAssertNil(manager.setLanguage(.fr, companyPath: root.path))
            let object = try XCTUnwrap(JSONSerialization.jsonObject(with: Data(contentsOf: file)) as? [String: Any])
            XCTAssertEqual(object["language"] as? String, "fr")
            XCTAssertEqual(object["count"] as? Int, 3)
            XCTAssertEqual((object["theme"] as? [String: Bool])?["dark"], true)
            let reloaded = LanguageManager()
            XCTAssertNil(reloaded.load(companyPath: root.path))
            XCTAssertEqual(reloaded.current, .fr)
            XCTAssertEqual(try FileManager.default.contentsOfDirectory(atPath: root.path), ["preferences.json"])
        }
    }

    func testInvalidPreferencesRejectLoadAndWriteWithoutMutation() async throws {
        let root = try fixture()
        try await MainActor.run {
            for text in ["broken", "[]", "null", #"{"language":"de"}"#, #"{"language":null}"#, #"{"language":42}"#] {
                let file = root.appendingPathComponent("preferences.json")
                let original = Data(text.utf8)
                try original.write(to: file)
                let manager = LanguageManager()
                XCTAssertNotNil(manager.load(companyPath: root.path), text)
                XCTAssertNotNil(manager.setLanguage(.fr, companyPath: root.path), text)
                XCTAssertEqual(manager.current, .en)
                XCTAssertEqual(try Data(contentsOf: file), original)
            }
        }
    }

    func testUnsafeOrMissingCompanyRejectedWithoutCreation() async throws {
        let root = try fixture()
        let link = root.appendingPathComponent("alias")
        try FileManager.default.createSymbolicLink(at: link, withDestinationURL: root)
        await MainActor.run {
            let manager = LanguageManager()
            for path in [root.appendingPathComponent("absent").path, link.path, "relative"] {
                XCTAssertNotNil(manager.setLanguage(.fr, companyPath: path))
                XCTAssertEqual(manager.current, .en)
            }
            XCTAssertFalse(FileManager.default.fileExists(atPath: root.appendingPathComponent("absent").path))
        }
    }

    func testSymlinkAndNonRegularPreferenceRejected() async throws {
        let root = try fixture()
        let external = try fixture().appendingPathComponent("original")
        let bytes = Data(#"{"language":"en"}"#.utf8)
        try bytes.write(to: external)
        let file = root.appendingPathComponent("preferences.json")
        try FileManager.default.createSymbolicLink(at: file, withDestinationURL: external)
        try await MainActor.run {
            let manager = LanguageManager()
            XCTAssertNotNil(manager.load(companyPath: root.path))
            XCTAssertNotNil(manager.setLanguage(.fr, companyPath: root.path))
            XCTAssertEqual(try Data(contentsOf: external), bytes)
            try FileManager.default.removeItem(at: external) // dangling link must also reject
            XCTAssertNotNil(manager.setLanguage(.fr, companyPath: root.path))
            try FileManager.default.removeItem(at: file)
            try FileManager.default.createDirectory(at: file, withIntermediateDirectories: false)
            XCTAssertNotNil(manager.setLanguage(.fr, companyPath: root.path))
            XCTAssertEqual(manager.current, .en)
        }
    }

    func testUnreadablePreferencesAndWriteFailurePreserveSelection() async throws {
        let root = try fixture()
        let file = root.appendingPathComponent("preferences.json")
        let bytes = Data("{}".utf8)
        try bytes.write(to: file)
        try await MainActor.run {
            let manager = LanguageManager()
            try FileManager.default.setAttributes([.posixPermissions: 0], ofItemAtPath: file.path)
            XCTAssertNotNil(manager.load(companyPath: root.path))
            XCTAssertNotNil(manager.setLanguage(.fr, companyPath: root.path))
            try FileManager.default.setAttributes([.posixPermissions: 0o600], ofItemAtPath: file.path)
            XCTAssertEqual(try Data(contentsOf: file), bytes)
            try FileManager.default.setAttributes([.posixPermissions: 0o500], ofItemAtPath: root.path)
            defer { try? FileManager.default.setAttributes([.posixPermissions: 0o700], ofItemAtPath: root.path) }
            XCTAssertNotNil(manager.setLanguage(.fr, companyPath: root.path))
            XCTAssertEqual(manager.current, .en)
            XCTAssertEqual(try Data(contentsOf: file), bytes)
        }
    }

    func testResourcesRejectUnsafeMissingAndDirectoryPathsWithoutOpening() throws {
        let root = try fixture()
        let outside = try fixture()
        let file = outside.appendingPathComponent("external.md")
        try Data("outside".utf8).write(to: file)
        try FileManager.default.createSymbolicLink(at: root.appendingPathComponent("escape"), withDestinationURL: outside)
        for path in [file.path, "../external.md", "escape/external.md", "missing.md", "."] {
            XCTAssertThrowsError(try ResourceLoader.resolvedFileURL(path, factorRoot: root.path))
            XCTAssertNotNil(ResourceLoader.openRelativePath(path, factorRoot: root.path, opener: { _ in XCTFail("Unsafe opener invoked"); return true }))
        }
        let local = root.appendingPathComponent("guide.md")
        try Data("local".utf8).write(to: local)
        var opened: URL?
        XCTAssertNil(ResourceLoader.openRelativePath("guide.md", factorRoot: root.path, opener: { opened = $0; return true }))
        XCTAssertEqual(opened, local)
        XCTAssertNotNil(ResourceLoader.openRelativePath("guide.md", factorRoot: root.path, opener: { _ in false }))
    }

    func testProductionManifestParsingRejectsMalformedEntriesAndSymlinkEscape() throws {
        let root = try fixture()
        let docs = root.appendingPathComponent("docs")
        try FileManager.default.createDirectory(at: docs, withIntermediateDirectories: false)
        let manifest = docs.appendingPathComponent("resources.json")
        XCTAssertNotNil(ResourceLoader.loadResources(factorRoot: root.path).error)
        for input in ["bad", "[]", #"{"schema_version":true,"resources":[]}"#, #"{"schema_version":2,"resources":[]}"#, #"{"schema_version":1,"resources":[{}]}"#] {
            try Data(input.utf8).write(to: manifest)
            XCTAssertNotNil(ResourceLoader.loadResources(factorRoot: root.path).error)
        }
        let valid = #"{"schema_version":1,"resources":[{"id":"guide","kind":"guide","language":"fr","title":{"en":"Guide","fr":"Guide"},"paths":{"en":"docs/guide.md","fr":"docs/guide.md"}}]}"#
        try Data(valid.utf8).write(to: manifest)
        let result = ResourceLoader.loadResources(factorRoot: root.path)
        XCTAssertNil(result.error)
        XCTAssertEqual(result.resources.count, 1)
        XCTAssertTrue(try XCTUnwrap(result.resources.first).isFrenchOnly)
        for replacement in ["/etc/hosts", "../escape.md"] {
            try Data(valid.replacingOccurrences(of: "docs/guide.md", with: replacement).utf8).write(to: manifest)
            XCTAssertNotNil(ResourceLoader.loadResources(factorRoot: root.path).error)
        }
        let external = try fixture().appendingPathComponent("manifest.json")
        try Data(valid.utf8).write(to: external)
        try FileManager.default.removeItem(at: manifest)
        try FileManager.default.createSymbolicLink(at: manifest, withDestinationURL: external)
        XCTAssertNotNil(ResourceLoader.loadResources(factorRoot: root.path).error)
    }

    func testActualLocalizationPreservesUnknownSourceData() {
        XCTAssertEqual(L.roomLabel("content", lang: .fr), "Contenu")
        XCTAssertEqual(L.statusDisplay("needs you", lang: .fr), "votre attention")
        XCTAssertEqual(L.statusDisplay("custom status", lang: .fr), "custom status")
        XCTAssertEqual(L.roomLabel("unknown", lang: .fr), "unknown")
    }
}

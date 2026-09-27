import AppKit
import Foundation

// MARK: - Resource model

struct FactorResource: Identifiable {
    let id: String
    let kind: String
    /// "bilingual", "en", "fr"
    let resourceLanguage: String
    let titleEN: String
    let titleFR: String
    let pathEN: String
    let pathFR: String

    var isFrenchOnly: Bool { resourceLanguage == "fr" }
}

// MARK: - ResourceLoader

/// Loads `docs/resources.json` relative to FACTOR_ROOT (or derived from FACTOR_WRITE_INTENT).
/// All file-system paths are validated as canonical contained paths before opening.
struct ResourceLoader {

    // MARK: Resolve manifest path

    /// Resolve the absolute path to `docs/resources.json`.
    static func manifestURL(factorRoot: String?) -> URL? {
        guard let root = factorRoot, !root.isEmpty else { return nil }
        let url = URL(fileURLWithPath: root)
            .appendingPathComponent("docs/resources.json")
        return url
    }

    static func factorRoot() -> String? {
        let env = ProcessInfo.processInfo.environment
        if let root = env["FACTOR_ROOT"]?.trimmingCharacters(in: .whitespacesAndNewlines),
           !root.isEmpty {
            return root
        }
        if let writeIntent = env["FACTOR_WRITE_INTENT"]?.trimmingCharacters(in: .whitespacesAndNewlines),
           !writeIntent.isEmpty {
            // Derive: FACTOR_WRITE_INTENT is <root>/scripts/write_intent.py
            let url = URL(fileURLWithPath: writeIntent)
            return url.deletingLastPathComponent().deletingLastPathComponent().path
        }
        return nil
    }

    // MARK: Load resources

    /// Load and parse the manifest. Returns nil + error string on failure.
    static func loadResources(factorRoot: String?) -> (resources: [FactorResource], error: String?) {
        guard let root = factorRoot else {
            return ([], "FACTOR_ROOT is not set.")
        }
        guard manifestURL(factorRoot: root) != nil else {
            return ([], "Could not build manifest path.")
        }
        let data: Data
        do {
            let checked = try resolvedFileURL("docs/resources.json", factorRoot: root)
            data = try Data(contentsOf: checked)
        } catch { return ([], "Resources manifest is missing, unsafe or unreadable.") }
        struct Manifest: Decodable {
            let schema_version: Int
            let resources: [Entry]
        }
        struct Entry: Decodable {
            let id: String
            let kind: String
            let language: String
            let title: [String: String]
            let paths: [String: String]
        }
        guard let manifest = try? JSONDecoder().decode(Manifest.self, from: data),
              manifest.schema_version == 1 else {
            return ([], "resources.json is malformed or unsupported.")
        }
        var results: [FactorResource] = []
        var ids = Set<String>()
        for item in manifest.resources {
            let id = item.id, kind = item.kind, lang = item.language
            guard !id.isEmpty, ids.insert(id).inserted, !kind.isEmpty,
                  ["en", "fr", "bilingual"].contains(lang),
                  let titleEN = item.title["en"], !titleEN.isEmpty,
                  let titleFR = item.title["fr"], !titleFR.isEmpty,
                  let pathEN = item.paths["en"], let pathFR = item.paths["fr"],
                  (try? containedURL(pathEN, factorRoot: root)) != nil,
                  (try? containedURL(pathFR, factorRoot: root)) != nil else {
                return ([], "resources.json contains an invalid resource.")
            }
            results.append(FactorResource(
                id: id,
                kind: kind,
                resourceLanguage: lang,
                titleEN: titleEN,
                titleFR: titleFR,
                pathEN: pathEN,
                pathFR: pathFR
            ))
        }
        return (results, nil)
    }

    // MARK: Open resource

    /// Open a resource file with NSWorkspace.
    /// Only opens files that exist inside `factorRoot` (canonical containment check).
    /// Returns an error string on failure, nil on success.
    @discardableResult
    static func openResource(
        _ resource: FactorResource,
        language: AppLanguage,
        factorRoot: String
    ) -> String? {
        let relativePath = language == .fr ? resource.pathFR : resource.pathEN
        return openRelativePath(relativePath, factorRoot: factorRoot)
    }

    /// Open a specific variant path relative to factorRoot.
    enum ResourceError: Error { case unsafePath, missingFile, openFailed }

    private static func containedURL(_ relativePath: String, factorRoot: String) throws -> URL {
        guard (factorRoot as NSString).isAbsolutePath,
              !relativePath.isEmpty, !(relativePath as NSString).isAbsolutePath,
              !relativePath.split(separator: "/").contains("..") else { throw ResourceError.unsafePath }
        let root = URL(fileURLWithPath: factorRoot).standardizedFileURL.resolvingSymlinksInPath()
        var isDirectory: ObjCBool = false
        guard FileManager.default.fileExists(atPath: root.path, isDirectory: &isDirectory), isDirectory.boolValue else {
            throw ResourceError.unsafePath
        }
        let file = root.appendingPathComponent(relativePath).standardizedFileURL.resolvingSymlinksInPath()
        guard file.path.hasPrefix(root.path + "/") else { throw ResourceError.unsafePath }
        return file
    }

    /// Shared by manifest reads and resource opens; resolves symlinks before containment.
    static func resolvedFileURL(_ relativePath: String, factorRoot: String) throws -> URL {
        let file = try containedURL(relativePath, factorRoot: factorRoot)
        let attributes = try FileManager.default.attributesOfItem(atPath: file.path)
        guard attributes[.type] as? FileAttributeType == .typeRegular,
              FileManager.default.isReadableFile(atPath: file.path) else { throw ResourceError.missingFile }
        return file
    }

    @discardableResult
    static func openRelativePath(
        _ relativePath: String, factorRoot: String,
        opener: (URL) -> Bool = { NSWorkspace.shared.open($0) }
    ) -> String? {
        do {
            let file = try resolvedFileURL(relativePath, factorRoot: factorRoot)
            guard opener(file) else { throw ResourceError.openFailed }
            return nil
        } catch { return "Resource could not be opened. Check its path and access permissions." }
    }
}

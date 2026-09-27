import Foundation
import Combine

enum AppLanguage: String, CaseIterable, Identifiable {
    case en, fr
    var id: String { rawValue }
    var displayName: String { self == .fr ? "Français" : "English" }
}

/// Company preferences use a single local writer. No cross-process locking is implied.
@MainActor
final class LanguageManager: ObservableObject {
    @Published private(set) var current: AppLanguage = .en
    private var sessionLanguage: AppLanguage = .en

    private enum PreferenceError: Error { case company, file, malformed, language }

    private func notice(_ error: Error, writing: Bool) -> String {
        let french = current == .fr
        let action = writing
            ? (french ? "Langue non enregistrée. " : "Language was not saved. ")
            : (french ? "Préférences non chargées. " : "Preferences were not loaded. ")
        let detail: String
        switch error as? PreferenceError {
        case .company:
            detail = french ? "Choisissez un dossier entreprise existant, sans lien symbolique." : "Choose an existing company directory without symbolic links."
        case .file:
            detail = french ? "preferences.json doit être un fichier ordinaire lisible, sans lien symbolique." : "preferences.json must be a readable regular file, not a symbolic link."
        case .malformed:
            detail = french ? "preferences.json doit contenir un objet JSON valide." : "preferences.json must contain a valid JSON object."
        case .language:
            detail = french ? "La langue doit être « en » ou « fr »." : "Language must be en or fr."
        default:
            detail = french ? "Vérifiez les droits d’accès au dossier et au fichier." : "Check access permissions for the directory and file."
        }
        return action + detail
    }

    /// Missing file/key means English, independently of the pre-company session choice.
    /// Invalid input leaves the active selection and the original bytes untouched.
    @discardableResult
    func load(companyPath: String?) -> String? {
        guard let companyPath else { current = sessionLanguage; return nil }
        do {
            let (_, preferences) = try readPreferences(companyPath: companyPath)
            current = (preferences["language"] as? String).flatMap(AppLanguage.init(rawValue:)) ?? .en
            return nil
        } catch { return notice(error, writing: false) }
    }

    @discardableResult
    func setLanguage(_ language: AppLanguage, companyPath: String?) -> String? {
        guard let companyPath else {
            sessionLanguage = language
            current = language
            return nil
        }
        do {
            let (url, existing) = try readPreferences(companyPath: companyPath)
            var preferences = existing
            preferences["language"] = language.rawValue
            let data = try JSONSerialization.data(withJSONObject: preferences, options: [.prettyPrinted, .sortedKeys])
            // Foundation creates a sibling temporary file and renames it atomically;
            // it supports both absent and existing destinations and propagates errors.
            try data.write(to: url, options: .atomic)
            current = language
            return nil
        } catch { return notice(error, writing: true) }
    }

    private func readPreferences(companyPath: String) throws -> (URL, [String: Any]) {
        guard (companyPath as NSString).isAbsolutePath else { throw PreferenceError.company }
        let root = URL(fileURLWithPath: companyPath).standardizedFileURL
        let fm = FileManager.default
        var component = root
        while component.path != "/" {
            let attributes = try fm.attributesOfItem(atPath: component.path)
            let type = attributes[.type] as? FileAttributeType
            // macOS exposes its temporary directories through these system aliases.
            let systemAlias = component != root && ["/var", "/tmp"].contains(component.path)
                && type == .typeSymbolicLink
            guard type == .typeDirectory || systemAlias else { throw PreferenceError.company }
            component.deleteLastPathComponent()
        }
        let url = root.appendingPathComponent("preferences.json")
        let attributes: [FileAttributeKey: Any]
        do { attributes = try fm.attributesOfItem(atPath: url.path) }
        catch let error as NSError where error.domain == NSCocoaErrorDomain && error.code == NSFileReadNoSuchFileError {
            return (url, [:])
        }
        guard attributes[.type] as? FileAttributeType == .typeRegular,
              fm.isReadableFile(atPath: url.path) else { throw PreferenceError.file }
        let data = try Data(contentsOf: url)
        guard let object = try? JSONSerialization.jsonObject(with: data),
              let preferences = object as? [String: Any] else { throw PreferenceError.malformed }
        if let value = preferences["language"] {
            guard let tag = value as? String, AppLanguage(rawValue: tag) != nil else { throw PreferenceError.language }
        }
        return (url, preferences)
    }
}

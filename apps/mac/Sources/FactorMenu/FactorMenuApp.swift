import AppKit
import SwiftUI

// MARK: - Localization

/// All user-visible strings keyed by language.
/// Company facts, protocol keys, intent payload fields are intentionally not translated.
enum L {
    static func str(_ en: String, _ fr: String, lang: AppLanguage) -> String {
        lang == .fr ? fr : en
    }

    static func menuTitle(lang: AppLanguage) -> String {
        str("Factor", "Factor", lang: lang)
    }
    static func chooseFolder(lang: AppLanguage) -> String {
        str("Choose a company folder.", "Choisissez un dossier entreprise.", lang: lang)
    }
    static func companyFolderPlaceholder(lang: AppLanguage) -> String {
        str("Company folder", "Dossier entreprise", lang: lang)
    }
    static func useThisFolder(lang: AppLanguage) -> String {
        str("Use this folder", "Utiliser ce dossier", lang: lang)
    }
    static func jobPlaceholder(lang: AppLanguage) -> String {
        str("Job", "Tâche", lang: lang)
    }
    static func submit(lang: AppLanguage) -> String {
        str("Submit", "Envoyer", lang: lang)
    }
    static func rollback(lang: AppLanguage) -> String {
        str("Rollback", "Annuler", lang: lang)
    }
    static func quit(lang: AppLanguage) -> String {
        str("Quit", "Quitter", lang: lang)
    }
    static func room(lang: AppLanguage) -> String {
        str("Room", "Espace", lang: lang)
    }
    static func language(lang: AppLanguage) -> String {
        str("Language", "Langue", lang: lang)
    }
    static func oneCompany(lang: AppLanguage) -> String {
        str(
            "This menu keeps one company folder.",
            "Ce menu n'autorise qu'un seul dossier entreprise.",
            lang: lang
        )
    }
    static func noCompanyError(lang: AppLanguage) -> String {
        str("Choose a company folder.", "Choisissez un dossier entreprise.", lang: lang)
    }
    static func noScriptError(lang: AppLanguage) -> String {
        str(
            "Set FACTOR_ROOT or FACTOR_WRITE_INTENT.",
            "Définissez FACTOR_ROOT ou FACTOR_WRITE_INTENT.",
            lang: lang
        )
    }

    // Room labels: display label (translated) — canonical tag stays in door.room.
    static func roomLabel(_ tag: String, lang: AppLanguage) -> String {
        switch tag {
        case "content":  return str("Content", "Contenu", lang: lang)
        case "numbers":  return str("Numbers", "Chiffres", lang: lang)
        case "growth":   return str("Growth", "Croissance", lang: lang)
        case "ads":      return str("Ads", "Publicités", lang: lang)
        case "partners": return str("Partners", "Partenaires", lang: lang)
        case "money":    return str("Money", "Finances", lang: lang)
        default:         return tag
        }
    }

    // Known waiting statuses from io/status.txt (source data preserved).
    static func statusDisplay(_ raw: String, lang: AppLanguage) -> String {
        if lang == .en { return raw }
        switch raw.lowercased() {
        case "waiting":    return "en attente"
        case "ready":      return "prêt"
        case "needs you":  return "votre attention"
        default:           return raw
        }
    }

    // Accessibility
    static func accessStatus(_ raw: String, lang: AppLanguage) -> String {
        str("Status \(raw)", "Statut \(statusDisplay(raw, lang: lang))", lang: lang)
    }
    static func accessJob(lang: AppLanguage) -> String {
        str("Job", "Tâche", lang: lang)
    }
    static func accessCompanyFolder(lang: AppLanguage) -> String {
        str("Company folder", "Dossier entreprise", lang: lang)
    }
    static func accessLanguagePicker(lang: AppLanguage) -> String {
        str("Language selector", "Sélecteur de langue", lang: lang)
    }
    static func accessMenuBarLabel(_ title: String, lang: AppLanguage) -> String {
        str("Factor \(title)", "Factor \(title)", lang: lang)
    }

    // Learning resources section
    static func learningTitle(lang: AppLanguage) -> String {
        str("Learning resources", "Ressources", lang: lang)
    }
    static func frenchOnlyBadge(lang: AppLanguage) -> String {
        str("· FR only", "· FR uniquement", lang: lang)
    }
    static func noFactorRoot(lang: AppLanguage) -> String {
        str(
            "Set FACTOR_ROOT to browse resources.",
            "Définissez FACTOR_ROOT pour accéder aux ressources.",
            lang: lang
        )
    }
    static func resourceNotFound(_ path: String, lang: AppLanguage) -> String {
        str("File not found: \(path)", "Fichier introuvable\u{00A0}: \(path)", lang: lang)
    }
    static func openEN(lang: AppLanguage) -> String {
        str("EN", "EN", lang: lang)
    }
    static func openFR(lang: AppLanguage) -> String {
        str("FR", "FR", lang: lang)
    }
}

// MARK: - AppDelegate

final class FactorAppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_: Notification) {
        DispatchQueue.main.async {
            NSApp.setActivationPolicy(.accessory)
        }
    }
}

// MARK: - Door (model)

@MainActor
final class Door: ObservableObject {
    @Published var menuTitle = "Factor"
    @Published var subtitle = "Factor"
    @Published var statusLine = "waiting"
    @Published var companyPath: String?
    @Published var job = ""
    @Published var room = "content"
    @Published var folderField = ""
    @Published var notice: String?
    @Published var stderrText: String?

    let rooms = ["content", "numbers", "growth", "ads", "partners", "money"]

    @Published private(set) var language: AppLanguage = .en
    let languageManager = LanguageManager()

    init() {
        reload()
    }

    func reload() {
        let path = readStoredPath()
        companyPath = path
        menuTitle = Self.folderName(path)
        notice = languageManager.load(companyPath: path)
        language = languageManager.current
        guard let path else {
            subtitle = "Factor"
            statusLine = "waiting"
            return
        }
        subtitle = whoLine(in: path)
        statusLine = readStatus(in: path)
    }

    func setLanguage(_ lang: AppLanguage) {
        let err = languageManager.setLanguage(lang, companyPath: companyPath)
        language = languageManager.current
        notice = err
    }

    func saveFolder() {
        notice = nil
        stderrText = nil
        if readStoredPath() != nil {
            notice = L.oneCompany(lang: language)
            return
        }
        let typed = folderField.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !typed.isEmpty else {
            notice = L.chooseFolder(lang: language)
            return
        }
        let expanded = (typed as NSString).expandingTildeInPath
        let absolute = (expanded as NSString).isAbsolutePath
            ? expanded
            : URL(fileURLWithPath: expanded).path
        let file = Self.pathFile()
        do {
            try FileManager.default.createDirectory(
                at: file.deletingLastPathComponent(),
                withIntermediateDirectories: true
            )
            try (absolute + "\n").write(to: file, atomically: true, encoding: .utf8)
            folderField = ""
            reload()
        } catch {
            notice = error.localizedDescription
        }
    }

    func submit() {
        stderrText = nil
        notice = nil
        guard let company = companyPath, !company.isEmpty else {
            stderrText = L.noCompanyError(lang: language)
            return
        }
        let sentence = job.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !sentence.isEmpty else { return }
        guard let script = writeIntentScript() else {
            stderrText = L.noScriptError(lang: language)
            return
        }
        let (code, err) = run(
            arguments: [
                "python3", script, company,
                "--sentence", sentence,
                "--room", room,
                "--door", "mac",
            ]
        )
        if code != 0 {
            stderrText = err.isEmpty ? "python3 exited \(code)" : err
            return
        }
        reload()
    }

    func rollback() {
        stderrText = nil
        notice = nil
        guard let company = companyPath, !company.isEmpty else { return }
        guard let script = rollbackScript() else { return }
        let (code, err) = run(arguments: ["python3", script, company])
        if code != 0 {
            stderrText = err.isEmpty ? "python3 exited \(code)" : err
            return
        }
        reload()
    }

    func rollbackScript() -> String? {
        for path in rollbackCandidates() where FileManager.default.fileExists(atPath: path) {
            return path
        }
        return nil
    }

    private func writeIntentScript() -> String? {
        if let given = env("FACTOR_WRITE_INTENT") {
            return given
        }
        if let root = env("FACTOR_ROOT") {
            return URL(fileURLWithPath: root)
                .appendingPathComponent("scripts/write_intent.py")
                .path
        }
        return nil
    }

    private func rollbackCandidates() -> [String] {
        var paths: [String] = []
        if let root = env("FACTOR_ROOT") {
            paths.append(
                URL(fileURLWithPath: root)
                    .appendingPathComponent("scripts/rollback.py")
                    .path
            )
        }
        if let given = env("FACTOR_WRITE_INTENT") {
            let scripts = (given as NSString).deletingLastPathComponent
            paths.append((scripts as NSString).appendingPathComponent("rollback.py"))
        }
        return paths
    }

    private func run(arguments: [String]) -> (Int32, String) {
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        process.arguments = arguments
        let errURL = FileManager.default.temporaryDirectory
            .appendingPathComponent("factor-intent-\(UUID().uuidString).err")
        FileManager.default.createFile(atPath: errURL.path, contents: nil)
        guard let handle = try? FileHandle(forWritingTo: errURL) else {
            try? process.run()
            process.waitUntilExit()
            return (process.terminationStatus, "")
        }
        process.standardError = handle
        try? process.run()
        process.waitUntilExit()
        handle.closeFile()
        let errText = (try? String(contentsOf: errURL, encoding: .utf8)) ?? ""
        try? FileManager.default.removeItem(at: errURL)
        return (process.terminationStatus, errText.trimmingCharacters(in: .whitespacesAndNewlines))
    }

    private func readStoredPath() -> String? {
        let file = Self.pathFile()
        guard let raw = try? String(contentsOf: file, encoding: .utf8) else { return nil }
        let line = raw.split(whereSeparator: \.isNewline).first.map(String.init) ?? ""
        let trimmed = line.trimmingCharacters(in: .whitespaces)
        guard !trimmed.isEmpty else { return nil }
        return (trimmed as NSString).expandingTildeInPath
    }

    private func whoLine(in company: String) -> String {
        let url = URL(fileURLWithPath: company).appendingPathComponent("instinct.md")
        guard let text = try? String(contentsOf: url, encoding: .utf8) else { return "Factor" }
        var inWho = false
        for raw in text.split(separator: "\n", omittingEmptySubsequences: false) {
            let line = raw.trimmingCharacters(in: .whitespacesAndNewlines)
            if line == "## Who" {
                inWho = true
                continue
            }
            if inWho {
                if line.hasPrefix("## ") { break }
                if !line.isEmpty { return line }
            }
        }
        return "Factor"
    }

    private func readStatus(in company: String) -> String {
        let url = URL(fileURLWithPath: company)
            .appendingPathComponent("io")
            .appendingPathComponent("status.txt")
        guard let text = try? String(contentsOf: url, encoding: .utf8) else { return "waiting" }
        for raw in text.split(whereSeparator: \.isNewline) {
            let line = raw.trimmingCharacters(in: .whitespaces)
            if !line.isEmpty { return line }
        }
        return "waiting"
    }

    private func env(_ name: String) -> String? {
        let value = ProcessInfo.processInfo.environment[name]?
            .trimmingCharacters(in: .whitespacesAndNewlines)
        guard let value, !value.isEmpty else { return nil }
        return value
    }

    private static func pathFile() -> URL {
        // Explicit development fixture override; the normal user path is unchanged.
        if let path = ProcessInfo.processInfo.environment["FACTOR_COMPANY_PATH_FILE"],
           (path as NSString).isAbsolutePath {
            return URL(fileURLWithPath: path)
        }
        return FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("Library/Application Support/Factor/company.path")
    }

    private static func folderName(_ path: String?) -> String {
        guard let path, !path.isEmpty else { return "Factor" }
        let name = path.split(separator: "/").last.map(String.init) ?? ""
        return name.isEmpty ? "Factor" : name
    }
}

// MARK: - LanguagePicker

struct LanguagePicker: View {
    @ObservedObject var door: Door

    var body: some View {
        Picker(L.language(lang: door.language), selection: Binding(
            get: { door.language },
            set: { door.setLanguage($0) }
        )) {
            ForEach(AppLanguage.allCases) { lang in
                Text(lang.displayName).tag(lang)
            }
        }
        .pickerStyle(.segmented)
        .accessibilityLabel(L.accessLanguagePicker(lang: door.language))
    }
}

// MARK: - LearningResourcesView

struct LearningResourcesView: View {
    let language: AppLanguage
    @State private var openError: String?

    private var factorRoot: String? { ResourceLoader.factorRoot() }

    private var resources: [FactorResource] {
        let (list, _) = ResourceLoader.loadResources(factorRoot: factorRoot)
        return list
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(L.learningTitle(lang: language))
                .font(.caption)
                .foregroundStyle(.secondary)

            if factorRoot == nil {
                Text(L.noFactorRoot(lang: language))
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            } else if resources.isEmpty {
                let (_, err) = ResourceLoader.loadResources(factorRoot: factorRoot)
                Text(err == nil ? L.noFactorRoot(lang: language) : L.str("Resources unavailable. Check the manifest and file paths.", "Ressources indisponibles. Vérifiez le manifeste et les chemins des fichiers.", lang: language))
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            } else {
                ScrollView {
                    VStack(alignment: .leading, spacing: 6) {
                        ForEach(resources) { resource in
                            ResourceRow(
                                resource: resource,
                                language: language,
                                factorRoot: factorRoot!,
                                openError: $openError
                            )
                        }
                    }
                }
                .frame(maxHeight: 180)
            }

            if let openError {
                Text(L.str(openError, "Impossible d’ouvrir la ressource. Vérifiez son chemin et les droits d’accès.", lang: language))
                    .font(.caption2)
                    .foregroundStyle(.red)
                    .fixedSize(horizontal: false, vertical: true)
                    .onTapGesture { self.openError = nil }
            }
        }
    }
}

// MARK: - ResourceRow

struct ResourceRow: View {
    let resource: FactorResource
    let language: AppLanguage
    let factorRoot: String
    @Binding var openError: String?

    private var displayTitle: String {
        language == .fr ? resource.titleFR : resource.titleEN
    }

    private var isFrOnlyForENUser: Bool {
        resource.isFrenchOnly && language == .en
    }

    var body: some View {
        HStack(spacing: 4) {
            // Title + optional FR-only badge
            Group {
                Text(displayTitle)
                    .font(.caption)
                if isFrOnlyForENUser {
                    Text(L.frenchOnlyBadge(lang: language))
                        .font(.caption2)
                        .foregroundStyle(.secondary)
                }
            }
            Spacer()
            // For bilingual resources show EN | FR buttons;
            // for FR-only show a single open button.
            if resource.resourceLanguage == "bilingual" {
                Button(L.openEN(lang: language)) {
                    openError = ResourceLoader.openRelativePath(resource.pathEN, factorRoot: factorRoot)
                }
                .buttonStyle(.borderless)
                .font(.caption2)
                .accessibilityLabel("\(displayTitle) EN")

                Button(L.openFR(lang: language)) {
                    openError = ResourceLoader.openRelativePath(resource.pathFR, factorRoot: factorRoot)
                }
                .buttonStyle(.borderless)
                .font(.caption2)
                .accessibilityLabel("\(displayTitle) FR")
            } else {
                // FR-only: single open button using the active language path
                Button(resource.isFrenchOnly ? "FR" : "EN") {
                    openError = ResourceLoader.openResource(resource, language: language, factorRoot: factorRoot)
                }
                .buttonStyle(.borderless)
                .font(.caption2)
                .accessibilityLabel(displayTitle)
            }
        }
    }
}

// MARK: - FactorMenu (view)

struct FactorMenu: View {
    @ObservedObject var door: Door
    @FocusState private var jobFocused: Bool

    var lang: AppLanguage { door.language }

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(door.menuTitle)
                .font(.headline)
            Text(door.subtitle)
                .font(.subheadline)

            // Language selector — always visible
            LanguagePicker(door: door)

            if door.companyPath != nil {
                // Status line: translated display, source data preserved in door.statusLine
                Text(L.statusDisplay(door.statusLine, lang: lang))
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .accessibilityLabel(L.accessStatus(door.statusLine, lang: lang))

                TextField(L.jobPlaceholder(lang: lang), text: $door.job)
                    .textFieldStyle(.roundedBorder)
                    .accessibilityLabel(L.accessJob(lang: lang))
                    .focused($jobFocused)

                // Room picker: translated labels, canonical tags as binding values
                Picker(L.room(lang: lang), selection: $door.room) {
                    ForEach(door.rooms, id: \.self) { tag in
                        Text(L.roomLabel(tag, lang: lang)).tag(tag)
                    }
                }
                .accessibilityLabel(L.room(lang: lang))

                Button(L.submit(lang: lang)) { door.submit() }
                    .keyboardShortcut(.defaultAction)
                    .disabled(door.job.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)

                if door.rollbackScript() != nil {
                    Button(L.rollback(lang: lang)) { door.rollback() }
                }
            } else {
                Text(L.chooseFolder(lang: lang))

                TextField(L.companyFolderPlaceholder(lang: lang), text: $door.folderField)
                    .textFieldStyle(.roundedBorder)
                    .accessibilityLabel(L.accessCompanyFolder(lang: lang))

                Button(L.useThisFolder(lang: lang)) { door.saveFolder() }
                    .keyboardShortcut(.defaultAction)
                    .disabled(
                        door.folderField.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
                    )
            }

            if let notice = door.notice, !notice.isEmpty {
                Text(notice)
                    .font(.caption)
                    .fixedSize(horizontal: false, vertical: true)
                    .textSelection(.enabled)
            }
            if let stderrText = door.stderrText, !stderrText.isEmpty {
                Text(stderrText)
                    .font(.caption)
                    .foregroundStyle(.red)
                    .fixedSize(horizontal: false, vertical: true)
                    .textSelection(.enabled)
            }

            Divider()

            // Learning resources section — available before and after company selection
            LearningResourcesView(language: lang)

            Divider()

            Button(L.quit(lang: lang)) {
                NSApplication.shared.terminate(nil)
            }
        }
        .padding(12)
        .frame(width: 320)
        .onAppear {
            door.reload()
            if door.companyPath != nil {
                jobFocused = true
            }
            if #available(macOS 14.0, *) {
                NSApp.activate()
            } else {
                NSApp.activate(ignoringOtherApps: true)
            }
        }
    }
}

// MARK: - App entry point

@main
struct FactorMenuApp: App {
    @NSApplicationDelegateAdaptor(FactorAppDelegate.self) private var appDelegate
    @StateObject private var door = Door()

    var body: some Scene {
        MenuBarExtra {
            FactorMenu(door: door)
        } label: {
            Label(door.menuTitle, systemImage: "circle.fill")
                .accessibilityLabel(L.accessMenuBarLabel(door.menuTitle, lang: door.language))
        }
        .menuBarExtraStyle(.window)
    }
}

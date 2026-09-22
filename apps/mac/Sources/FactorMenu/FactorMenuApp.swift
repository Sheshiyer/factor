import AppKit
import SwiftUI

final class FactorAppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_: Notification) {
        DispatchQueue.main.async {
            NSApp.setActivationPolicy(.accessory)
        }
    }
}

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

    private let oneCompany = "This menu keeps one company folder."

    init() {
        reload()
    }

    func reload() {
        let path = readStoredPath()
        companyPath = path
        menuTitle = Self.folderName(path)
        guard let path else {
            subtitle = "Factor"
            statusLine = "waiting"
            return
        }
        subtitle = whoLine(in: path)
        statusLine = readStatus(in: path)
    }

    func saveFolder() {
        notice = nil
        stderrText = nil
        if readStoredPath() != nil {
            notice = oneCompany
            return
        }
        let typed = folderField.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !typed.isEmpty else {
            notice = "Choose a company folder."
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
            stderrText = "Choose a company folder."
            return
        }
        let sentence = job.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !sentence.isEmpty else { return }
        guard let script = writeIntentScript() else {
            stderrText = "Set FACTOR_ROOT or FACTOR_WRITE_INTENT."
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
            return (1, "Could not record the command error.")
        }
        process.standardOutput = FileHandle.nullDevice
        process.standardError = handle
        do {
            try process.run()
        } catch {
            try? handle.close()
            try? FileManager.default.removeItem(at: errURL)
            return (1, error.localizedDescription)
        }
        process.waitUntilExit()
        try? handle.close()
        let text = (try? String(contentsOf: errURL, encoding: .utf8)) ?? ""
        try? FileManager.default.removeItem(at: errURL)
        return (
            process.terminationStatus,
            text.trimmingCharacters(in: .whitespacesAndNewlines)
        )
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
        FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("Library/Application Support/Factor/company.path")
    }

    private static func folderName(_ path: String?) -> String {
        guard let path, !path.isEmpty else { return "Factor" }
        let name = path.split(separator: "/").last.map(String.init) ?? ""
        return name.isEmpty ? "Factor" : name
    }
}

struct FactorMenu: View {
    @ObservedObject var door: Door
    @FocusState private var jobFocused: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(door.menuTitle)
                .font(.headline)
            Text(door.subtitle)
                .font(.subheadline)
            if door.companyPath != nil {
                Text(door.statusLine)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .accessibilityLabel("Status \(door.statusLine)")
                TextField("Job", text: $door.job)
                    .textFieldStyle(.roundedBorder)
                    .accessibilityLabel("Job")
                    .focused($jobFocused)
                Picker("Room", selection: $door.room) {
                    ForEach(door.rooms, id: \.self) { name in
                        Text(name).tag(name)
                    }
                }
                Button("Submit") { door.submit() }
                    .keyboardShortcut(.defaultAction)
                    .disabled(door.job.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                if door.rollbackScript() != nil {
                    Button("Rollback") { door.rollback() }
                }
            } else {
                Text("Choose a company folder.")
                TextField("Company folder", text: $door.folderField)
                    .textFieldStyle(.roundedBorder)
                    .accessibilityLabel("Company folder")
                Button("Use this folder") { door.saveFolder() }
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
            Button("Quit") {
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

@main
struct FactorMenuApp: App {
    @NSApplicationDelegateAdaptor(FactorAppDelegate.self) private var appDelegate
    @StateObject private var door = Door()

    var body: some Scene {
        MenuBarExtra {
            FactorMenu(door: door)
        } label: {
            Label(door.menuTitle, systemImage: "circle.fill")
                .accessibilityLabel("Factor \(door.menuTitle)")
        }
        .menuBarExtraStyle(.window)
    }
}

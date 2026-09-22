// swift-tools-version: 5.7
import PackageDescription

let package = Package(
    name: "FactorMenu",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(name: "FactorMenu", targets: ["FactorMenu"])
    ],
    targets: [
        .executableTarget(name: "FactorMenu")
    ]
)

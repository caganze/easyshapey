# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.4] - 2025-01-07

### Added
- **Polygon class**: Support for arbitrary N-sided 2D polygons (triangles to any N)
- Interactive polygon creation via `Polygon.from_clicks()`
- Data-fitted polygons via `Polygon.from_data()` with convex_hull and bounding_box methods
- Comprehensive test suite for Polygon class

### Changed
- Streamlined codebase following [Abseil performance principles](https://abseil.io/fast/hints.html)
- Updated all docstrings to consistent NumPy style
- Improved rotation algorithm efficiency (reduced iterations from 1000 to 100)
- Cleaner, leaner implementation with ~40% less code

## [0.0.3] - 2025-01-07

### Security
- Fixed deprecated pandas `.ix[]` indexer usage by replacing with `.loc[]` in `selector.py` (2 instances)
  - This resolves compatibility issues with newer pandas versions and improves code security
- Updated SECURITY.md with proper vulnerability reporting guidelines and project-specific information

### Changed
- Updated supported version information in SECURITY.md to reflect actual project version

## [0.0.2] - Previous Release

### Changed
- Version bump and package updates

## [0.0.1] - Initial Release

### Added
- Initial release of easyshapey package
- Core shape manipulation functionality
- Box and Oval shape classes
- Selector class for shape-based data selection

# Development Tools

This directory contains various tools and utilities for Elysian Nexus development.

## Directory Structure

- `build/` - Build tools and scripts
  - `packager/` - Game packaging tools
  - `asset_processor/` - Asset processing tools
  - `dependency_checker/` - Dependency management tools

- `debug/` - Debugging tools
  - `profilers/` - Performance profiling tools
  - `loggers/` - Enhanced logging utilities
  - `inspectors/` - State inspection tools

- `deploy/` - Deployment tools
  - `installers/` - Installation package creators
  - `updaters/` - Update management tools
  - `validators/` - Deployment validation tools

- `automation/` - Automation tools
  - `test_runners/` - Automated testing tools
  - `build_automation/` - CI/CD tools
  - `asset_management/` - Asset automation tools

- `profiling/` - Performance analysis tools
  - `memory/` - Memory usage analysis
  - `cpu/` - CPU usage analysis
  - `network/` - Network performance tools

## Usage Guidelines

1. **Build Tools**
   ```bash
   python tools/build/packager/create_release.py
   python tools/build/asset_processor/process_assets.py
   ```

2. **Debug Tools**
   ```bash
   python tools/debug/profilers/profile_game.py
   python tools/debug/inspectors/inspect_state.py
   ```

3. **Deployment Tools**
   ```bash
   python tools/deploy/installers/create_installer.py
   python tools/deploy/validators/validate_build.py
   ```

## Development Guidelines

1. Keep tools modular and focused
2. Include documentation and usage examples
3. Write tests for tools
4. Maintain backward compatibility
5. Log tool operations appropriately 
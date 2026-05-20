# LightweightSyslog

A lightweight tool that logs basic system metrics on MacOS at regular intervals and optionally runs as a user-level systemd service.

Features
Logs system uptime, CPU usage, and memory usage.
Writes logs to ~/logger.log.
Can run continuously as a user-level launchd service.
Self-contained and easy to set up.

## Requirements

MacOS



## Usage

Run the release to avoid installing dependencies

Usage Examples

Run locally and log to file only:


```./syslog```


Send logs to a server while running:


```./syslog --server http://example.com/log-receiver```


Setup systemd service for automatic logging:


```./syslog --setup-service```

You can also combine server logging with systemd setup:

```./syslog --setup-service --server http://example.com/log-receiver```

## Features
The tool will:

Create a systemd user service at ~/Library/LaunchAgents/com.user.loggerpy
Enable and start the service, which ensures the logger runs automatically on login.
Log system uptime, CPU, and memory usage to ~/logger.log.


Logs in ~/logger.log.

Running as a launchd Service

The script automatically sets up a user-level launchd service:

~/Library/LaunchAgents/com.user.loggerpy

## Security and Privacy

This script only collects system metrics and only transmits data externally when the user requests it to a user selected location.


## Contributing

Contributions are welcome! Please submit issues or pull requests for bug fixes and feature enhancements.


## License

This project is licensed under the MIT License.

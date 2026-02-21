import os
import subprocess

# Allowed paths for disk usage inspection – prevents OS command injection by
# accepting only a whitelist of safe mount points instead of passing raw user
# input directly to a shell.
ALLOWED_PATHS = {
    "/",
    "/tmp",
    "/var",
    "/home",
    "/app",
    "/data",
}


def get_disk_usage(parameters: str):
    # Validate that the requested path is in the allowed set; reject anything else.
    path = parameters.strip() if parameters else "/"
    if path not in ALLOWED_PATHS:
        raise ValueError(
            f"Path '{path}' is not permitted. Allowed paths: {sorted(ALLOWED_PATHS)}"
        )

    try:
        result = subprocess.run(
            ["df", "-h", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
        usage = result.stdout.strip().decode()
    except Exception:
        raise Exception("An unexpected error was observed")

    return usage

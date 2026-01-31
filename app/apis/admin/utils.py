import re
import subprocess


def get_disk_usage(parameters: str):
    """
    Get disk usage information with protection against command injection.
    Only allows specific safe parameters.
    """
    # Sanitize input: only allow alphanumeric, forward slashes, and hyphens
    # for safe filesystem paths
    if parameters and not re.match(r'^[a-zA-Z0-9/_-]+$', parameters):
        raise ValueError("Invalid parameters: only alphanumeric characters, '/', '_', and '-' are allowed")
    
    # Build command as a list to avoid shell injection
    # Only allow specific safe options
    command = ["df", "-h"]
    
    # If parameters provided, validate it's a safe path
    if parameters:
        # Additional validation: ensure no command chaining or special characters
        if any(char in parameters for char in [';', '|', '&', '$', '`', '\n', '\r']):
            raise ValueError("Invalid characters in parameters")
        command.append(parameters)

    try:
        # Use shell=False and pass command as list to prevent injection
        result = subprocess.run(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            shell=False,
            timeout=5  # Add timeout to prevent hanging
        )
        usage = result.stdout.strip().decode()
    except subprocess.TimeoutExpired:
        raise Exception("Command execution timed out")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

    return usage

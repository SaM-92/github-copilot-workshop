import re
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Code Analysis Tools")

@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"

@mcp.tool()
async def check_variable_naming(code: str) -> dict:
    """Check variable names to ensure they follow snake_case format (name_name)
    
    Args:
        code: The code to analyze
        
    Returns:
        A dictionary with the analysis results containing:
        - is_valid: Whether all variable names follow snake_case
        - violations: List of variable names that don't follow snake_case
        - line_numbers: Dictionary mapping variable names to their line numbers
    """
    result = {
        "is_valid": True,
        "violations": [],
        "line_numbers": {}
    }
    
    # Regex to find variable assignments
    var_pattern = re.compile(r'(\w+)\s*=')
    # Regex to check if a name is in snake_case
    snake_case_pattern = re.compile(r'^[a-z][a-z0-9_]*$')
    
    lines = code.split('\n')
    for line_num, line in enumerate(lines, 1):
        # Skip comments
        if line.strip().startswith('#'):
            continue
            
        matches = var_pattern.findall(line)
        for var_name in matches:
            # Skip if it's a Python keyword or builtin
            if var_name in ['if', 'for', 'while', 'def', 'class', 'else', 'elif', 'return']:
                continue
                
            if not snake_case_pattern.match(var_name):
                result["is_valid"] = False
                if var_name not in result["violations"]:
                    result["violations"].append(var_name)
                    result["line_numbers"][var_name] = line_num
    
    return result

@mcp.tool()
async def check_security_leakages(code: str) -> dict:
    """Check code for potential security leakages like API keys, tokens, etc.
    
    Args:
        code: The code to analyze
        
    Returns:
        A dictionary with the analysis results containing:
        - has_leakages: Whether any potential security leakages were found
        - findings: List of potential security issues
        - line_numbers: Dictionary mapping issues to their line numbers
    """
    result = {
        "has_leakages": False,
        "findings": [],
        "line_numbers": {}
    }   
    
    # Patterns to check for various security leakages
    patterns = {
        "api_key": re.compile(r'api.?key.?=.?["\']([a-zA-Z0-9_\-]{20,})["\']', re.IGNORECASE),
        "access_token": re.compile(r'(access.?token|auth.?token|token).?=.?["\']([a-zA-Z0-9_\-\.]{20,})["\']', re.IGNORECASE),
        "password": re.compile(r'password.?=.?["\'](.+)["\']', re.IGNORECASE),
        "connection_string": re.compile(r'(connection.?string).?=.?["\'](.+)["\']', re.IGNORECASE),
        "storage_key": re.compile(r'(storage.?key|storage.?account.?key).?=.?["\'](.+)["\']', re.IGNORECASE),
        "secret": re.compile(r'secret.?=.?["\'](.+)["\']', re.IGNORECASE),
        "private_key": re.compile(r'-----BEGIN (\w+) PRIVATE KEY-----', re.IGNORECASE)
    }
    
    lines = code.split('\n')
    for line_num, line in enumerate(lines, 1):
        # Skip comments
        if line.strip().startswith('#'):
            continue
            
        for issue_type, pattern in patterns.items():
            matches = pattern.findall(line)
            if matches:
                result["has_leakages"] = True
                finding = f"{issue_type} found"
                result["findings"].append(finding)
                result["line_numbers"][finding] = line_num
    
    return result

if __name__ == "__main__":
    mcp.run()
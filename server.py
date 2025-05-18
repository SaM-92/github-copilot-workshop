from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")

@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"


@mcp.tool()
async def add_list_of_numbers(numbers: list[int]) -> int:
    """Add a list of numbers"""
    return sum(numbers)


@mcp.tool()
async def add_two_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get weather information for a city"""
    return f"The weather in {city} is sunny."




if __name__ == "__main__":
    mcp.run()
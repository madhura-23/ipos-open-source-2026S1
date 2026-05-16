import asyncio

from fastmcp.prompts.base import PromptResult

from main import mcp  # MCP server instance


# This est simulates a Client LLM connection
async def main():
    # Get the prompt template from the MCP server
    prompt = await mcp.get_prompt("explain_conversion")
    assert prompt is not None

    # Render it with the arguments
    result = await prompt.render({
        "input_value": "3",
        "input_unit": "miles",
        "target_unit": "km",
    })
    assert isinstance(result, PromptResult)

    # result.messages contains the list of rendered Message objects
    for msg in result.messages:
        print(f"Role: {msg.role}")
        print(f"Content:\n{msg.content}\n")
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())

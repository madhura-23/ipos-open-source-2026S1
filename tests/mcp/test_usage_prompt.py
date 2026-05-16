import asyncio

from fastmcp.prompts.base import PromptResult

from main import mcp


async def main():
    prompt = await mcp.get_prompt("api_usage")
    assert prompt is not None

    api_reference = """Available endpoints:
- GET /health → Check server status
- POST /convert → Convert between units
- GET /history → View recent conversions"""

    result = await prompt.render({
        "operation": "convert",
        "resource_text": api_reference,
    })
    assert isinstance(result, PromptResult)

    print(f"Resource provided to the model:\n{api_reference}\n")

    if hasattr(result, "messages"):
        for msg in result.messages:
            if hasattr(msg, "content"):
                print(f"[{msg.role.upper()}]")
                content = (
                    msg.content.text
                    if hasattr(msg.content, "text")
                    else str(msg.content)
                )
                if isinstance(content, str):
                    print(content.strip())
                else:
                    print(content)
                print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

"""Small stdio MCP client; accepts tool name and a JSON argument file."""
import asyncio, json, os, sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    root=Path(os.environ.get('STS2_MCP_ROOT',r'C:\Tools\sts2-modding-mcp'))
    args=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8-sig')) if len(sys.argv)>2 else {}
    params=StdioServerParameters(command=str(root/'venv/Scripts/python.exe'),args=[str(root/'run.py')],cwd=str(root),env=dict(os.environ,PYTHONUTF8='1',DOTNET_ROLL_FORWARD='Major',DOTNET_CLI_UI_LANGUAGE='en-US'))
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            reply=await session.call_tool(sys.argv[1],args)
            failed=reply.isError
            for content in reply.content:
                if content.type=='text':
                    print(content.text)
                    try:
                        result=json.loads(content.text)
                        failed=failed or result.get('success') is False or bool(result.get('error'))
                    except json.JSONDecodeError: pass
    if failed: raise SystemExit(1)
asyncio.run(main())

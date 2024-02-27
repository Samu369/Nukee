import discord

# --- Discord Checks ---
async def check_token(token: str):
    client = discord.Client(intents=discord.Intents.default())
    try:
        await client.login(token)
        await client.close()
        return True
    except discord.errors.LoginFailure:
        return False

async def check_server(token: str, server_id:int):
    client = discord.Client(intents=discord.Intents.default())
    ret = False
    
    @client.event
    async def on_ready():
        nonlocal ret
        server = client.get_guild(server_id)
        if server is not None:
            ret = True
        await client.close()
        
    await client.start(token)
    return ret
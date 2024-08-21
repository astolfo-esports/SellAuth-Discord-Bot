import discord
from discord.ext import commands
import requests

TOKEN = 'YOUR TOKEN' # Replace With Your Bot Token
API_BASE_URL = 'https://api.sellauth.com/v1'
API_TOKEN = 'https://beta.sellauth.com/user' # Replace With Your SellAuth User

bot = commands.Bot(command_prefix='/')

def call_api(endpoint, method='GET', data=None):
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    url = f'{API_BASE_URL}{endpoint}'
    r = requests.request(method, url, headers=headers, json=data)
    return r.json()

@bot.command()
async def check_order(ctx, order_id):
    r = call_api(f'/shops/{order_id}/invoices')
    await ctx.send(f'Order: {r}')

@bot.command()
async def claim_customer_role(ctx, order_id):
    r = call_api(f'/shops/{order_id}/invoices')
    if r:
        role = discord.utils.get(ctx.guild.roles, name='Customer')
        if role:
            await ctx.author.add_roles(role)
            await ctx.send(f'Gave you {role.name} role')
        else:
            await ctx.send('Role not found lol')
    else:
        await ctx.send('Nope, invalid order ID')

@bot.command()
async def create_coupon(ctx, shop_id, discount):
    r = call_api(f'/shops/{shop_id}/coupon', 'POST', {'discount': discount})
    await ctx.send(f'Created: {r}')

@bot.command()
async def delete_coupon(ctx, shop_id, coupon_id):
    r = call_api(f'/shops/{shop_id}/coupons/{coupon_id}', 'DELETE')
    await ctx.send(f'Deleted: {r}')

@bot.command()
async def delete_product(ctx, shop_id, product_id):
    r = call_api(f'/shops/{shop_id}/products/{product_id}', 'DELETE')
    await ctx.send(f'Gone: {r}')

@bot.command()
async def edit_product_price(ctx, shop_id, product_id, price):
    r = call_api(f'/shops/{shop_id}/products/{product_id}/update', 'PATCH', {'price': price})
    await ctx.send(f'Updated: {r}')

@bot.command()
async def help(ctx):
    await ctx.send("""
    /check_order <order_id> - Check order
    /claim_customer_role <order_id> - Get role
    /create_coupon <shop_id> <discount> - New coupon
    /delete_coupon <shop_id> <coupon_id> - Remove coupon
    /delete_product <shop_id> <product_id> - Remove product
    /edit_product_price <shop_id> <product_id> <price> - Change price
    """)

bot.run(TOKEN)

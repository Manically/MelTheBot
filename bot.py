import discord
from discord.ext import commands, tasks
import random
import json

@client.command()
async def cmds(ctx):
    em = discord.Embed(title='Economy Commands',color=discord.Color.red())
    em.add_field(name='_balance',value='Tells you your balance.')
    em.add_field(name='_withdraw',value='Withdraws from your bank.')
    em.add_field(name='_deposit',value='Deposits to your bank.')
    em.add_field(name='_beg',value='Gives you money')
    em.add_field(name='_slots',value='Spins the slot machine.')
    em.add_field(name='_givemoney',value='Sends money to another player.')
    await ctx.send(embed=em)

client = commands.Bot(command_prefix=")")

@client.command(aliases=['bal'])
async def balance(ctx):
    await openacc(ctx.author)
    user = ctx.author
    users = await getdata()
    
    walletamt = users[str(user.id)]['wallet']
    bankamt = users[str(user.id)]['bank']
    
    em = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.red())
    em.add_field(name = 'Wallet balance',value = walletamt)
    em.add_field(name = 'Bank balance',value = bankamt)
    await ctx.send(embed = em)

async def openacc(user):
    users = await getdata()
    
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 100
        users[str(user.id)]['bank'] = 1000
    
    with open('bank.json', 'w') as f:
        json.dump(users,f)

async def getdata():
    with open('bank.json', 'r') as f:
        users = json.load(f)
    return users

@client.command()
async def beg(ctx):
    user = ctx.author
    await openacc(ctx.author)
    users = await getdata()
    earnings = random.randrange(101)
    await ctx.send(f'Someone gave {ctx.author.name} {earnings} MelBux!')
    users[str(user.id)]['wallet'] += earnings
    with open('bank.json','w') as f:
        json.dump(users,f)
    return True

async def updatebank(user,change=0,mode='wallet'):
    users = await getdata()
    users[str(user.id)][mode] += change
    with open('bank.json', 'w') as f:
        json.dump(users,f)
    bal = [[str(user.id)]['wallet'],[str(user.id)]['bank']]
    return user

@client.command()
async def withdraw(ctx,amount = None):
    await openacc(ctx.author)
    if amount == None:
        await ctx.send('Please enter the amount you want to withdraw.')
        return
    bal = await updatebank(ctx.author)
    amount = str(amount)
    if amount>bal[1]:
        await ctx.send('That amount is too big!')
        return
    if amount<0:
        await ctx.send('The amount must be above 0.')
        return
    await updatebank(ctx.author,amount)
    await updatebank(ctx.author,-1*amount,'bank')
    await ctx.send(f'{ctx.author.name} withdrew {amount} MelBux.')

@client.command(aliases=['dep'])
async def deposit(ctx,amount = None):
    await openacc(ctx.author)
    if amount == None:
        await ctx.send('Please enter the amount you want to deposit.')
        return
    bal = await updatebank(ctx.author)
    amount = str(amount)
    if amount>bal[0]:
        await ctx.send('That amount is too big!')
        return
    if amount<0:
        await ctx.send('The amount must be above 0.')
        return
    await updatebank(ctx.author,-1*amount)
    await updatebank(ctx.author,amount,'bank')
    await ctx.send(f'{ctx.author.name} deposited {amount} MelBux.')

@client.command(aliases=['pay','sendmoney','send','give','paymoney'])
async def givemoney(ctx,member:discord.Member,amount = None):
    await openacc(ctx.author)
    await openacc(member)
    if amount == None:
        await ctx.send('Please enter the amount you want to pay.')
        return
    bal = await updatebank(ctx.author)
    amount = str(amount)
    if amount>bal[0]:
        await ctx.send('That amount is too big!')
        return
    if amount<0:
        await ctx.send('The amount must be above 0.')
        return
    await updatebank(ctx.author,-1*amount,'bank')
    await updatebank(member,amount,'bank')
    await ctx.send(f'{ctx.author.name} gave {amount} MelBux to {member.name}.')

@client.command(aliases=['slot'])
async def slots(ctx,amount = None):
    await openacc(ctx.author)
    if amount == None:
        await ctx.send('Please enter the amount you want to bet.')
        return
    bal = await updatebank(ctx.author)
    amount = str(amount)
    if amount>bal[0]:
        await ctx.send('That amount is too big!')
        return
    if amount<0:
        await ctx.send('The amount must be above 0.')
        return
    final = []
    for i in range(3):
        a = random.choice(['0','7','O'])
        final.append(a)
    await ctx.send(str(final))
    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
        await updatebank(ctx.author,2*amount)
        await ctx.send(f'{ctx.author.name} won!')
    else:
        await updatebank(ctx.author,-1*amount)
        await ctx.send(f'{ctx.author.name} lost!')

client.run(token)

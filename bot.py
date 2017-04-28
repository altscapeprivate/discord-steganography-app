import discord
import steganography as steg
import asyncio
import threading
import config as conf

client = discord.Client()
user_vars = dict()


def not_pm(message):
    return type(message.channel).__name__ == "Channel"
	
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
	if message.content.startswith('\\\\'):
		if(message.content.startswith('\\\\>')):
			print(message.content)
			print(steg.get_encoded)
		if not not_pm(message):
			print(message.author.name + ": " + steg.decode(message.content.encode('utf8').decode('utf8')))
		else:
			print(message.author.nick + ": " + steg.decode(message.content.encode('utf8').decode('utf8')))

			
def help(args):
	print("quit being a retard")
	return ''

def test(args):
	print(args)
	
def stop(args):
	asyncio.run_coroutine_threadsafe(client.close(), client.loop).result()
	exit()
	return
	
def send(args):
	id = args[0]
	message = ''.join( (str + ' ') for str in args[1:])
	message = message[:-1]
	asyncio.run_coroutine_threadsafe(client.send_message(discord.Object(id=id), message), client.loop)
	return 'sent'
	
# def send_dm(args):
	# ## currently not working
	# id = args[0]
	# message = args[1]
	# asyncio.run_coroutine_threadsafe(client.send_message(discord.Member(id=id), message), client.loop)
	
def space(args):
	message = args[0]
	space = steg.get_space(message)
	print("%d bytes of space for encoding in the message" % (space))
	return space
	
def encode(args):
	message = args[1]
	secret = args[0]
	encoded = '\\\\'.join(steg.hide_message(secret,message))
	return encoded
	
def define(args):	
	name = args[0]
	value = args[1]
	if(name[0] == '$'):
		user_vars[name] = value
	else:
		print("variable must begin with $")
	return ''
	

def parse(msg):
	input=msg.split(' ')
	y=1
	
	command = input[0]
	arg = ''
	file_input = ''
	file_output = ''
	pipe = ''
	
	while y<len(input):
		if (input[y]=='<'):
			file_input = input[y+1]
			y+=1
		elif (input[y]=='<'):
			file_output = input[y+1]
			y+=1
		elif (input[y]=='|'):
			str = ''.join(s + ' ' for s in input[y+1:])
			pipe = parse(str[:-1])
			break
		else:
			arg+=' ' + input[y]
		y+=1
	
	return (command,arg,file_input,file_output,pipe)
	
	

def parse_args(arg):
	x = 1
	y = 0
	args = []
	current_arg = ''
	arg_is_string = False
	var_name = ''
	inString = False
	while x<len(arg):
		if (arg[x]=='\'') | (arg[x]=='\"'):
			inString = not inString
		elif (inString):
			arg_is_string = True
			if(arg[x]=='\\'):
				x+=1
			current_arg+=arg[x]
		elif (arg[x]==' '):
			if not arg_is_string:
				for key in user_vars:
					current_arg = current_arg.replace(key,user_vars[key])
			args.append(current_arg)
			current_arg=''
			arg_is_string = False
			y+=1
		else:
			current_arg+=arg[x]
		
		x+=1
	
	for key in user_vars:
		current_arg = current_arg.replace(key,user_vars[key])
	args.append(current_arg)
	#print(current_arg)
	return args

def run_com(command):
	add_args = ''
	func = possible_functions.get(command[0])
		
	if(command[2] != ''):
		with open(command[2], 'r', encoding="utf8") as in_file:
			add_args = in_file.read()
	
	args = parse_args(command[1] + " " + add_args)
	output = func(args)
	
	if(command[3] != ''):
		with open(command[3], 'w+', encoding="utf8") as out_file:
			out_file.write(output)
		
	if(command[4] != ''):
		new_com = (command[4][0], command[4][1] + ' ' + str(output)) + command[4][2:]
		run_com(new_com)
		
	return output
		
	
t = threading.Thread(target=client.run, args=(conf.EMAIL,conf.PASS))
t.start()
possible_functions = globals().copy()
possible_functions.update(locals())

print("Enter commands with command name, followed by arguments space seperated. Type help for more details")

while True:
	command = input()
	command = parse(command)
	try:
		run_com(command)
	except Exception as e:
		print(e)



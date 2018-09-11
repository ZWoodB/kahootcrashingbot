import praw
import subprocess
import os
import config

def init():
	try:
		DB = open("processed.txt", "r")
		DB.close()
	except:
		DB = open("processed.txt", "w+")
		DB.close()

def main():
	print ('Logging in\n')
	reddit = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = config.user_agent)
	
	subreddit = reddit.subreddit(config.target_subreddit)		
	for submission in subreddit.stream.submissions():
		proctitle = processtitle(submission)
		if proctitle and submissioncheck(submission):
			savesubmission(submission)
			runbot(submission, proctitle)
			print('Successfully ran bot on game [', submission.title, ']\n\n','--------------------------------------------------------------------------------\n')
		
		if proctitle and not submissioncheck(submission):
			print('Post [',submission.title,'] has already been processed\n\n','--------------------------------------------------------------------------------\n')
		
		if not proctitle and submissioncheck(submission):
			savesubmission(submission)
			print('Post [',submission.title,'] was too short, ignoring post\n\n','--------------------------------------------------------------------------------\n')
		
		if not proctitle and not submissioncheck(submission):
			print('Post [',submission.title,'] was both too short and already processed\n\n','--------------------------------------------------------------------------------\n')

def runbot(submission, proctitle):
	reply = ('###Attempting to flood game *' + proctitle[0] + '* with *' + proctitle[2] + '* bots named *' + proctitle[1] + '* \n \n ___ \n \n ^(I am a bot, this action was performed automatically.) \n \n^(If you have any questions please contact my developer, u/PMMEURTHROWAWAYS) \n \n^(All of my code is visible here: https://github.com/cymug/kahootcrashingbot)')
	submission.reply(reply)
	print('Replied to:',submission.title,'\n')
	command = (r'go run [botdirectory] ' + proctitle[0] + ' ' + proctitle[1] + ' ' + proctitle[2])
	bot = subprocess.Popen(command)
	print(bot)

def submissioncheck(submission):
	DB = open("processed.txt", "r")
	IDs = DB.read()
	if submission.id in IDs:
		DB.close()
		return False

	DB.close()
	return True

def savesubmission(submission):
	DB = open("processed.txt", "a")
	DB.write('[' + submission.id + ' , "' + submission.title + '"] - ')
	print('Saved submission [', submission.title, ']\n')
	DB.close()

def processtitle(submission):
	processedtitle = submission.title.split(" | ", 4)
	shorttitle = processedtitle[:3]
	if len(shorttitle) == 3:
		return processedtitle
	else:
		return False

init()

if __name__ == '__main__':
	main()


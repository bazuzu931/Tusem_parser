import os


for dir in os.listdir("./list"):
	to_file = './list/' + dir

	for file in os.listdir(to_file):
		if '.txt' in file:
			file_path = to_file + '/' + file

			
			with open(file_path) as f:
				for link in f:
					command = "youtube-dl --output '~/Desktop/TUSEM_2/list/" + dir + "/%(title)s.%(ext)s' " + str(link) + " -c"
					os.system(command)
					












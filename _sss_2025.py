#! /bin/python3

# creates index.md
# converts index
# generate rss for posts

import os
import shutil
import pypandoc
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup
import pytz
from email.utils import format_datetime

root_url = "https://archibaldgrey.com/"

tumblr = "https://www.tumblr.com/blog/archiethegreyt"
mastodon = "two"
bluesky = "three"
github = "four"

rss_header = "<?xml version=\"1.0\" encoding=\"utf-8\"?><rss version=\"2.0\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:content=\"http://purl.org/rss/1.0/modules/content/\" xmlns:atom=\"http://www.w3.org/2005/Atom\"><channel><atom:link href=\"https://archibaldgrey.com/rss.xml\" rel=\"self\" type=\"application/rss+xml\" /><title>Archie's Blog</title><link>https://www.archibaldgrey.com</link><description>The Blog and Newsletter of Archibald Grey</description>"
rss_footer = "</channel></rss>"
rss_post_list = []



today = date.today()
d1 = today.strftime("%d/%m/%Y")

input_dir = "input/"
output_dir = "output/"

non_index_HTML_template = "templates/_html_template_input.html"
non_index_HTML_template_output = "templates/_html_template_output.html"

index_HTML_template = "templates/_index_template_input.html"
index_HTML_template_output = "templates/_index_template_output.html"

index_MD_template = "templates/_index_input.md"
index_MD_template_output = "templates/_index_output.md"
index_output = "output/index.html"

input_dir_list = os.listdir(input_dir)

#############################
### CREATE OUTPUT FOLDERS ###
#############################

os.makedirs(os.path.join(output_dir,"posts"), exist_ok=True)
os.makedirs(os.path.join(output_dir,"pages"), exist_ok=True)
os.makedirs(os.path.join(output_dir,"fonts"), exist_ok=True)
os.makedirs(os.path.join(output_dir,"images"), exist_ok=True)

##########################################Links############################
### POPULATE NAV LIST FROM PAGES FOLDER AND INSERT INTO ACTIVE TEMPLATE ###
###########################################################################

### POPULATE ###

pages_dir = os.path.join(input_dir, "pages")
pages_dir_list = os.listdir(pages_dir)
pages_dir_list.sort()

pages_link_list_index = "<ul>"
pages_link_list_index += "<li><a href=\"index.html\">updates</a></li>"
pages_link_list_non_index = "<ul>"
pages_link_list_non_index += "<li><a href=\"../index.html\">updates</a></li>"

tumblr = "<li><a href=\"" + tumblr + "\" target=\"_blank\">tumblr</a></li>"
mastodon = "<li><a href=\"" + mastodon + "\" target=\"_blank\">mastodon</a></li>"
bluesky = "<li><a href=\"" + bluesky + "\" target=\"_blank\">bluesky</a></li>"
github = "<li><a href=\"" + github + "\" target=\"_blank\">github</a></li>"

social_links = tumblr + mastodon + bluesky + github

for page in pages_dir_list:
	if page.startswith("_"):
		continue
	page_link_index = "<li><a href=\"pages/" + page.replace(".md", ".html") + "\">" + page.replace(".md","") + "</a></li>"
	page_link_non_index = "<li><a href=\"../pages/" + page.replace(".md", ".html") + "\">" + page.replace(".md","") + "</a></li>"

	pages_link_list_index += page_link_index
	pages_link_list_non_index += page_link_non_index

pages_link_list_index += social_links
pages_link_list_index += "</ul>"
pages_link_list_non_index += social_links
pages_link_list_non_index += "</ul>"

### WRITE NON-INDEX TEMPLATE ###

with open(non_index_HTML_template, "r+") as HTML_template:
	HTML_input = HTML_template.read() # read everything in the file

HTML_output = HTML_input.replace("NAVIGATION", pages_link_list_non_index)

writeFile = open(non_index_HTML_template_output, mode='w', encoding="utf8")
writeFile.write(HTML_output)
writeFile.close()

### WRITE INDEX TEMPLATE ###

with open(index_HTML_template, "r+") as HTML_template:
	HTML_input = HTML_template.read() # read everything in the file

HTML_output = HTML_input.replace("NAVIGATION", pages_link_list_index)

writeFile = open(index_HTML_template_output, mode='w', encoding="utf8")
writeFile.write(HTML_output)
writeFile.close()

#####################
### CONVERT FILES ###
#####################

for input_dir_list_item in input_dir_list:
	
	inputMD =""
	outputHTML = ""

	if input_dir_list_item.startswith("_") or input_dir_list_item.startswith(".") or input_dir_list_item == "index.md":
		continue

	elif input_dir_list_item == "pages":
		print("DIR :: PAGES")

		for page in pages_dir_list:
			if page.startswith("_") or page.startswith("."):
				continue
			print("\tProcessing :: " + page)
			if not post.endswith(".md"):
				print("Not markdown")
				continue
			inputMD = os.path.join(pages_dir,page)
			outputHTML = page.replace(".md",".html")
			outputHTML = os.path.join(output_dir,"pages",outputHTML)
			output = pypandoc.convert_file(inputMD, 'html', extra_args=["--template=templates/_html_template_output.html"], outputfile=outputHTML)


	elif input_dir_list_item == "posts":
		print("DIR :: POSTS")
		posts_dir = os.path.join(input_dir, input_dir_list_item)
		posts_dir_list = os.listdir(posts_dir)
		for post in posts_dir_list:
			if post.startswith("_") or post.startswith("."):
				continue
			print("\tProcessing :: " + post)
			if not post.endswith(".md"):
				print("Not markdown")
				continue
			inputMD = os.path.join(posts_dir,post)
			outputHTML = post.replace(".md",".html")
			outputHTML = os.path.join(output_dir,"posts",outputHTML)
			output = pypandoc.convert_file(inputMD, 'html', extra_args=["--template=templates/_html_template_output.html"], outputfile=outputHTML)

	elif input_dir_list_item == "images":
		print("DIR :: image")
		images_dir = os.path.join(input_dir, input_dir_list_item)
		images_dir_list = os.listdir(images_dir)
		for image in images_dir_list:
			if image.startswith("."):
				continue
			print("\t" + image)
			shutil.copy(os.path.join(images_dir,image), os.path.join(output_dir,"images",image))


	elif input_dir_list_item == "fonts":
		print("DIR :: FONTS")
		fonts_dir = os.path.join(input_dir, input_dir_list_item)
		fonts_dir_list = os.listdir(fonts_dir)
		for font in fonts_dir_list:
			if font.startswith("."):
				continue
			print("\t" + font)
			#print(os.path.join(fonts_dir,font))
			#print(os.path.join(output_dir,font))
			shutil.copy(os.path.join(fonts_dir,font), os.path.join(output_dir,"fonts",font))
	else:
		print(input_dir_list_item)

########################
### index page stuff ###
########################

print("CREATING index.md\n")

posts_output_dir = "output/posts"
posts_output_dir_list = os.listdir(posts_output_dir)
posts_output_dir_list.sort(reverse=True)

posts_list = ""

for post in posts_output_dir_list:
	if post.startswith("_"):
		continue
	print("\tProcessing :: " + post)

	post_path = os.path.join(posts_output_dir, post)

	# print(post_path)

	with open(post_path, 'r') as input_data:
		soup = BeautifulSoup(input_data, 'html.parser')

	html_title = soup.title.string

	description = soup.find("meta", property="description")

	cover = soup.find("meta", property="cover")

	date = soup.find('meta', attrs={'name': 'created'})
	dt = datetime.strptime(date["content"], "%Y-%m-%d")
	eastern = pytz.timezone("US/Eastern")	
	dt = eastern.localize(dt)
	rfc822_date = format_datetime(dt)

	content = soup.find('main')

	content_html = content.decode_contents().replace("../",root_url)

	# print(content_html)

	# print("DESCRIPTION :: " + description["content"])
	
	################
	### MARKDOWN ###
	################

	list_item_div_start = "<div class=\"list_item_wrap\">\n"

	list_item_div_end = "\n</div>"

	cover_image = cover["content"]

	post_date = "\n<div class=\"post_date\">" + date["content"] + "</div>"

	cover_image_content = "\n<div class=\"list_page_item_cover\"><a href=\"" + post_path.replace("output/","") + "\"><img src=\"" + cover_image.replace("../","") + "\" class=\"list_page_item_cover_img\"></a></div>"

	link_title = "\n\n<div class=\"list_page_item_link\">" + "<h2>[" + html_title + "](" + post_path.replace("output/","") + ")</h2>" + "</div>"

	description_content = "\n\n<div class=\"list_page_item_desc\">[" + description["content"] + "](" + post_path.replace("output/","") + ")</div>"

	post_item = list_item_div_start + link_title + post_date + cover_image_content + description_content + list_item_div_end + "\n\n"

	posts_list += post_item

	#########################
	### POPULATE RSS LIST ###
	#########################

# IMAGES NOT WORKING, both cover and inside post

	content = "<content:encoded><![CDATA[" + content_html + "]]></content:encoded>"

	rss_item = "<item><title>" + html_title + "</title><link>https://archibaldgrey.com/" + post_path.replace("output/","") + "</link><pubDate>" + rfc822_date + "</pubDate><guid>https://archibaldgrey.com/" + post_path.replace("output/","") + "</guid><description>" + description["content"] + "</description>" + content + "</item>"

	rss_post_list.append(rss_item)

### WRITE INDEX TEMPLATE ###

with open(index_MD_template, "r+") as MD_template:
	MD_input = MD_template.read() # read everything in the file

MD_output = MD_input.replace("BODY_CONTENT", posts_list)

#print(MD_output)

writeFile = open(index_MD_template_output, mode='w', encoding="utf8")
writeFile.write(MD_output)
writeFile.close()

output = pypandoc.convert_file(index_MD_template_output, 'html', extra_args=["--template=templates/_index_template_output.html"], outputfile=index_output)




################
### RSS FEED ###
################

rss_posts = ""


for item in rss_post_list:

	rss_posts += item

rss_contents = rss_header + rss_posts + rss_footer

with open("output/rss.xml", "w+") as rss_output:
	rss_output.write(rss_contents)
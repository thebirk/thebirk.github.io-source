import os
import copy
import json
import jinja2 as jinja
import shutil
import pathlib
import datetime
import subprocess
import distutils.dir_util as dir_util

# Metadata variables
# 
# 'custom-style':
#  A list of strings that will be inserted ass css into the HTML output
#   useful for custom styling of certain elements.


# 1. Read metadata from all posts
#  - Using pandoc is overkill fix this.
# 2. Template and generate the posts
#  - No real need for templating
# 3. Template and generate posts index.html
#  - Uses jinja to display all the posts
# 4. Template and generate index.html
#  - Uses jinja to only display the 3 most recent posts


# Dependencies:
# - Python 3.7
# - Pandoc with support for the '--metadata-file' option
# - Jinja2


output_path_str = './output'
output_path = pathlib.Path(output_path_str)

posts_dir = './posts'
static_resources_path = pathlib.Path('./static')
navbar_template = './navbar.html'
post_template = './html_template.html'
metadata_template = './html_template_metadata.html'
css = './markdown.css.html'

posts_path = output_path.joinpath('posts')

# These variables will be available inside the template
global_pandoc_vars = {
	'base_url': 'http://thebirk.net/',
	'post_path': str(posts_path.relative_to(output_path)),
	'year': str(datetime.datetime.now().year),
}

# List of all posts
posts = []


def gen_posts_index():
	print("posts/index.html")
	with open(posts_path.joinpath('index.html.pre'), mode='w') as f:
		f.flush()

	index_params = [
		'pandoc',
		'-s',
		'--section-divs',
		'--mathjax',
		'-H', css,
		'-A', str(posts_path.joinpath('index.html.pre')),
		'--template', post_template,
		'-o', str(posts_path.joinpath('index.html')),
	]

	for key, value in global_pandoc_vars.items():
			index_params.append('-V')
			index_params.append('{}:{}'.format(key, value))

	preprocessed = preprocess_markdown('posts_index.md', global_pandoc_vars)

	subprocess.run(index_params, check=True, input=preprocessed)

	os.remove(posts_path.joinpath('index.html.pre'))


def get_metadata_for_file(path):
	# We could avoid a pandoc pass by simply parsing the header
	# Doing this for now as it keeps dependencies down and the header parsing identical
	json_result = subprocess.run([
		'pandoc',
		'-s',
		'-t', 'html',
		'-f', 'markdown',
		'--template', metadata_template,
		path
	], check=True, capture_output=True)

	metadata = json.loads(json_result.stdout)

	return metadata


def gen_index():
	print("index.html")
	with open(output_path.joinpath('index.html.pre'), mode='w') as f:
		f.write('<p>Here are my most recent blog posts:</p>')
		
		total = min(3, len(posts))
		posts_to_list = posts[:total]

		f.write('<ul>')
		for p in posts_to_list:
			f.write('<li>')
			f.write('{} - '.format(p['date']))
			f.write('<a href="{}">'.format((p['path'])))
			f.write(p['title'])
			f.write("</a>")
			f.write("</li>")

		f.write('<li><a href="{}">More</a></li>'.format('/' + (posts_path.relative_to(output_path).as_posix())))
		f.write('</ul>')


	index_params = [
		'pandoc',
		'-s',
		'--section-divs',
		'--mathjax',
		'-H', css,
		'-A', str(output_path.joinpath('index.html.pre')),
		'--template', post_template,
		'-o', str(output_path.joinpath('index.html')),
	]

	for key, value in global_pandoc_vars.items():
			index_params.append('-V')
			index_params.append('{}:{}'.format(key, value))

	index_params.append('index.md')
	subprocess.run(index_params, check=True)

	metadata = get_metadata_for_file('index.md')

	os.remove(output_path.joinpath('index.html.pre'))


def preprocess_file(path, vars):
	file_text = path.read_text()
	template = jinja.Template(file_text)
	result = template.render(vars)
	return result


def preprocess_markdown(path, vars):
	params = [
		'pandoc',
		'--metadata-file=test.meta.json',
		'--template', path,
	]

	for key, value in vars.items():
			params.append('-V')
			params.append('{}:{}'.format(key, value))

	params.append(path)
	result = subprocess.run(params, check=True, capture_output=True)

	return result.stdout


def copy_static_resources():
	print('{}/*'.format(static_resources_path))
	static_resources_path.mkdir(exist_ok=True)
	dir_util.copy_tree(str(static_resources_path), str(output_path))


def gen_posts_metadata():
	# Grab list of all posts in posts_dir
	posts_list = list(pathlib.Path(posts_dir).glob("*.md"))
	posts_path.mkdir(exist_ok=True)

	print("Generating metadata for posts:")

	for index, path in enumerate(posts_list):
		print('({}/{})'.format(index+1, len(posts_list)), path)

		meta = get_metadata_for_file(str(path))
		output_html = posts_path.joinpath('{}.html'.format(path.stem))

		post = meta
		post['path'] = '/' + output_html.relative_to(output_path).as_posix()
		posts.append(post)

	# Sort posts after date, assumes well formed dates
	posts.sort(key=lambda p: p['date'], reverse=True)

	# Output metadata for all posts
	with open('test.meta.json', mode='w') as f:
		f.write('{')

		f.write('"posts": [')
		for p in posts:
			f.write('{')
			f.write(f'"title": "{p["title"]}",')
			f.write(f'"path": "{p["path"]}",')
			f.write(f'"date": "{p["date"]}",')
			f.write('},')
		f.write(']')

		f.write('}')


def gen_posts():
	# Grab list of all posts in posts_dir
	posts_list = list(pathlib.Path(posts_dir).glob("*.md"))
	posts_path.mkdir(exist_ok=True)

	print("Generating posts:")

	for index, path in enumerate(posts_list):
		print('({}/{})'.format(index+1, len(posts_list)), path)

		preprocessed = preprocess_markdown(str(path), global_pandoc_vars)

		output_html = posts_path.joinpath('{}.html'.format(path.stem))
		params = [
			'pandoc',
			'-s',
			'--section-divs',
			'--mathjax',
			'-H', css,
			'--template', post_template,
			'-o', str(output_html),
			'-f', 'markdown',
			'--highlight-style=zenburn'
		]

		for key, value in global_pandoc_vars.items():
			params.append('-V')
			params.append('{}:{}'.format(key, value))

		# params.append(str(path))
		# print(params)
		subprocess.run(params, check=True, input=preprocessed)


def main():
	# Ensure output_path exists and is empty
	shutil.rmtree(output_path, ignore_errors=True)
	os.makedirs(output_path_str, exist_ok=True)


	gen_posts_metadata()
	gen_posts()
	gen_posts_index()
	gen_index()

	copy_static_resources()

#	temp_text = """\
#{% for post in posts[0:3] %}
#- [{{post.title}}]({{post.path}}) - {{post.date}} {% endfor %}
#"""
#
#	temp = jinja.Template(temp_text)
#	print(temp.render(posts=posts))


if __name__ == '__main__':
	main()
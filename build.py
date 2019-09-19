import os
import json
import shutil
import pathlib
import datetime
import subprocess

# Metadata variables
# 
# 'custom-style':
#  A list of strings that will be inserted ass css into the HTML output
#   useful for custom styling of certain elements.
#
# 'resources':
#  A list of files that will be moved to the same folder as the HTML output
#   the path to the files should be relative.

output_path_str = './output'
output_path = pathlib.Path(output_path_str)

posts_dir = './posts'
navbar_template = './navbar.html'
post_template = './html_template.html'
metadata_template = './html_template_metadata.html'
css = './markdown.css'

posts_path = output_path.joinpath('posts')

# These variables will be available inside the template
global_pandoc_vars = {
	'base_url': 'http://thebirk.net/',
	'post_path': str(posts_path.relative_to(output_path)),
	'year': str(datetime.datetime.now().year),
}

# List of all posts
posts = []

def get_path_as_relative(path):
	#TODO: This should be renamed to something like get_path_as_relative_link() or something as all
	#      it does it make sure the path with '/' thus making it relative to the website root
	return '/' + str(path)

def gen_posts_index():
	print("posts/index.html")
	with open(posts_path.joinpath('index.html.pre'), mode='w') as f:
		f.write('<p>All posts</p>')
		f.write("<ul>")

		for p in posts:
			f.write('<li><a href="{}">'.format(get_path_as_relative(p['path'])))
			f.write(p['title'])
			f.write("</a>")
			f.write(' - {}'.format(p['date']))
			f.write("</li>")
		f.write("</ul>")

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

	index_params.append('posts_index.md')

	subprocess.run(index_params, check=True)

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
			f.write('<a href="{}">'.format(get_path_as_relative(p['path'])))
			f.write(p['title'])
			f.write("</a>")
			f.write("</li>")

		f.write('<li><a href="{}">More</a></li>'.format(get_path_as_relative(posts_path.relative_to(output_path))))
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
	print(metadata)

	os.remove(output_path.joinpath('index.html.pre'))


def preprocess_markdown(path, vars):
	params = [
		'pandoc',
		'--template', path,
	]

	for key, value in vars.items():
			params.append('-V')
			params.append('{}:{}'.format(key, value))

	params.append(path)
	result = subprocess.run(params, check=True, capture_output=True)

	return result.stdout


def copy_resources(metadata, src_path, dst_path):
	pass


def gen_posts():
	# Grab list of all posts in posts_dir
	posts_list = list(pathlib.Path(posts_dir).glob("*.md"))
	posts_path.mkdir(exist_ok=True)

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

		json_result = subprocess.run([
			'pandoc',
			'-s',
			'-t', 'html',
			'-f', 'markdown',
			'--template', metadata_template,
			str(path)
		], check=True, capture_output=True)

		post = json.loads(json_result.stdout)
		post['path'] = output_html.relative_to(output_path)
		posts.append(post)

	# Sort posts after date, assumes well formed dates
	posts.sort(key=lambda p: p['date'], reverse=True)


def main():
	# Ensure output_path exists and is empty
	shutil.rmtree(output_path, ignore_errors=True)
	os.makedirs(output_path_str, exist_ok=True)

	# Copy CNAME to output
	shutil.copyfile('CNAME', output_path.joinpath('CNAME'))
	#shutil.copyfile('anchor.min.js', output_path.joinpath('anchor.min.js'))

	gen_posts()
	gen_posts_index()
	gen_index()


if __name__ == '__main__':
	main()
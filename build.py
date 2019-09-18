import json
import os
import pathlib
import subprocess
import shutil


output_path_str = './output'
output_path = pathlib.Path(output_path_str)

posts_dir = './posts'
navbar_template = './navbar.html'
post_template = './html_template.html'
metadata_template = './html_template_metadata.html'
css = './markdown.css'


# Ensure output_path exists and is empty
shutil.rmtree(output_path, ignore_errors=True)
os.makedirs(output_path_str, exist_ok=True)

# Grab list of all posts in posts_dir
posts_list = list(pathlib.Path(posts_dir).glob("*.md"))
posts_path = output_path.joinpath('posts')
posts_path.mkdir(exist_ok=True)

# These variables will be available inside the template
custom_pandoc_vars = {
	'base_url': 'http://thebirk.net/',
	'post_path': str(posts_path.relative_to(output_path)),
}

custom_pandoc_vars['base_url'] = 'localhost'

# List of all posts
posts = []

for index, path in enumerate(posts_list):
	print('({}/{})'.format(index+1, len(posts_list)), path)
	output_html = posts_path.joinpath('{}.html'.format(path.stem))
	params = [
		'pandoc',
		'-s',
		'--section-divs',
		'--mathjax',
		'-H', css,
		'--template', post_template,
		'-o', str(output_html),
	]

	for key, value in custom_pandoc_vars.items():
		params.append('-V')
		params.append('{}:{}'.format(key, value))

	params.append(str(path))
	# print(params)
	subprocess.run(params, check=True)

	json_result = subprocess.run([
		'pandoc',
		'-s',
		'-t', 'html',
		'-f', 'markdown',
		'--template', metadata_template,
		# '-o', str(output_html.with_suffix('.json')),
		str(path)
	], check=True, capture_output=True)

	post = json.loads(json_result.stdout)
	post['path'] = output_html.relative_to(output_path)
	posts.append(post)


def get_path_as_relative(path):
	return '/' + str(path)


posts.sort(key=lambda p: p['date'], reverse=True)


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

	for key, value in custom_pandoc_vars.items():
			index_params.append('-V')
			index_params.append('{}:{}'.format(key, value))

	index_params.append('posts_index.md')

	subprocess.run(index_params, check=True)


gen_posts_index()

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

	for key, value in custom_pandoc_vars.items():
			index_params.append('-V')
			index_params.append('{}:{}'.format(key, value))

	index_params.append('index.md')

	subprocess.run(index_params, check=True)

gen_index()
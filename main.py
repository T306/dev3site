from quart import Quart, render_template, request, send_from_directory, abort
import mysql.connector
import os

app = Quart(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

db = mysql.connector.connect(
	host=os.environ['db_addr'],
	user=os.environ['db_user'],
	password=os.environ['db_pass'],
	database=os.environ['db_db']
)

cursor = db.cursor(dictionary=True)


@app.route('/')
async def home():
	cursor.execute('SELECT * FROM Projects')
	project_list = cursor.fetchall()
	return await render_template("pages/home.html", title='Home', page='/', projects=project_list)


@app.route('/projects')
async def projects():
	cursor.execute('SELECT * FROM Projects')
	project_list = cursor.fetchall()
	return await render_template("pages/projects.html", title='Projects', projects=project_list, page='/projects')


@app.route('/project/<path:path>')
async def project(path):
	try:
		cursor.execute('SELECT * FROM Projects WHERE title = ' + '\'' + path + '\'')
		content = cursor.fetchall()
		return await render_template('pages/project-temp.html', project=content, title=path)
	except IndexError:
		abort(404)


@app.route('/about')
async def about():
	return await render_template("pages/about.html", title='About', page='/about')


@app.route('/manifest.json', methods=['GET'])
@app.route('/sitemap.xml', methods=['GET'])
async def static_from_root():
	return await send_from_directory(app.static_folder, request.path[1:])


# Error Handling

# noinspection PyUnusedLocal
@app.errorhandler(404)
async def page_not_found(error):
	return await render_template('errors/404.html'), 404


app.run(host='0.0.0.0', port=81)

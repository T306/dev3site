from quart import Quart, render_template, request, send_from_directory, abort
import os
from surrealdb import db

app = Quart(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/')
async def home():
    return await render_template("pages/home.html", title='Home', page='/')


@app.route('/projects')
async def projects():
    projectlist = db('SELECT * FROM project')[0]['result']
    return await render_template("pages/projects.html",
                                 title='Projects',
                                 projects=projectlist,
                                 page='/projects')


@app.route('/project/<path:path>')
async def project(path):
    try:
        project = db('SELECT * FROM project WHERE title = ' + '\'' + path + '\'')[0]['result'][0]
        return await render_template('pages/project-temp.html', project=project, title=path)
    except IndexError:
        abort(404)


@app.route('/about')
async def about():
    return await render_template("pages/about.html", title='About', page='/about')


@app.route('/manifest.json', methods=['GET'])
@app.route('/sitemap.xml', methods=['GET'])
async def static_from_root():
    return await send_from_directory(app.static_folder, request.path[1:])


# Errors

@app.errorhandler(404)
async def page_not_found(error):
    return await render_template('errors/404.html'), 404


app.run(host='0.0.0.0', port=81)

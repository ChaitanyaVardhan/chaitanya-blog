from flask import(
    Blueprint, g, flash, redirect, url_for,
    render_template, request
)

from app.db import get_db

from app.auth import login_required


bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id FROM '
        'Post p JOIN User u ON p.author_id = u.id '
        'ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']

        error = None
        db = get_db()
        db.execute(
            'INSERT INTO Post (title, body, author_id) '
            'VALUE (?, ?, ?) ', (title, body, g.user['id'])
        )
        db.commit()
        return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']

        error = None

        if not title:
            error = "Title is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'Update Post SET title = ?, body = ?, '
                'WHERE id = ?', (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM Post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

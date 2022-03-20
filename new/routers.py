from new import app, db
from flask import render_template, request, redirect
from new.models import Article


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html', title="Главная страница")


@app.route("/about")
def about():
    return render_template('about.html', title="О сайте")


@app.route("/create_article", methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')

        except:
            return 'Про отправки прозашло ошибка!'

    else:
        return render_template('create_article.html', title="Создать статью")


@app.route("/posts")
def posts():
    article = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', title="Статьи", article=article)


@app.route("/post/<int:id>")
def post(id):
    post = Article.query.get(id)
    return render_template('post_articl.html', title=post.title, post=post)


@app.route("/post/<int:id>/del")
def post_deleted(id):
    post = Article.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Про отправки прозашло ошибка!'


@app.route("/post/<int:id>/update", methods=['POST', 'GET'])
def update_article(id):
    post = Article.query.get(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.intro = request.form['intro']
        post.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')

        except:
            return 'Про отправки прозашло ошибка!'

    else:
        return render_template('post_update.html', title="Создать статью", post=post)


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title='Страница не найден')
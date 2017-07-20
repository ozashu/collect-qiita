from flask import Flask, request, render_template, redirect, session, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from .forms import EmailPasswordForm, EmailForm, UsernamePasswordForm
from .models import User, Fav
# from .util import ts, send_email
#from . import app, db, redis_store
from . import app, db, cache
import requests

url = "http://qiita.com/api/v2/items?page=1&per_page=100"
data = requests.get(url).json()

def get_model_dict(model):
    return dict((column.name, getattr(model, column.name))
        for column in model.__table__.columns)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = UsernamePasswordForm()

    if form.validate_on_submit():
#        user = User.login(form.username.data, form.password.data)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user.is_correct_password(form.password.data):
#            redis_store.set('username', request.form['username'])
#            login_user(user, form.remember_me.data)
            session['auth.user'] = get_model_dict(user) 
            login_user(user)
            return redirect(url_for('.get_qiita'))
        else:
            return redirect(url_for('.login'))
        return render_template('login.html', form=form)

        if user is None:
            flash('ユーザー名とパスワードの組み合わせが違います。')
            return redirect(url_for('.login'))
            
        session['auth.user'] = get_model_dict(user) 
        return redirect(url_for('.get_qiita'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
#    redis_store.set('username', '')
    logout_user()
    session.clear()

    return redirect(url_for('.login'))

@app.route('/signup', methods=["GET", "POST"])
@cache.cached(timeout=600)
def signup():
    form = EmailPasswordForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('ユーザー登録が完了しました。ログインして下さい')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/')
def get_qiita():
    """
    Get newest Qiita Articles
    """
    articles = []
    for article in data:
        articles.append(dict(title=article["title"],
                         user_id=article["user"]["id"],
                         user_image=article["user"]["profile_image_url"],
                         url=article["url"]
                         ))
    return render_template('index.html', articles=articles)
#    return render_template('index.html', articles=articles, user=redis_store.get('username'))
#    return render_template('index.html', articles=articles, user=redis_store.get('username'),fav=fav)

@app.route('/', methods=['POST'])
def search_qiita():
    """Serch newest Qiita Articles
    """
    searched_result = [] # empty list
    keyword = request.form['keyword'] # Get form Keyword

    for article in data:
        search_article = dict(title=article["title"],
                            user_id=article["user"]["id"],
                            user_image=article["user"]["profile_image_url"],
                            url=article["url"]
                            )
        if keyword in search_article['title']:
            searched_result.append(search_article)
        if keyword in search_article['user_id']:
            searched_result.append(search_article)

#    return render_template('search_result.html', searched_result=searched_result, user=redis_store.get('username').decode("utf-8"))
    return render_template('search_result.html', searched_result=searched_result)

if __name__ == '__main__':
        app.run(host='localhost',debug=True)

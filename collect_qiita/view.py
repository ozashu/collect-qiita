from flask import Flask, request, render_template, redirect, session, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from .forms import EmailPasswordForm, EmailForm, UsernamePasswordForm
from .models import User, Fav
# from .util import ts, send_email
from . import app, db, redis_store
import requests

"""
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signup"
"""

url = "http://qiita.com/api/v2/items?page=1&per_page=100"
data = requests.get(url).json()

"""
@app.before_request
def before_request():
    # already login
    if redis_store.get('username') is not None:
        return
    else:
        return redirect(url_for('login'))
    # login page
    if request.path == '/login':
        return
    #staticファイルはリダイレクトしないように
    if request.path.count('/static'):
        return
    # user need login
    return redirect('/login')
"""

def get_model_dict(model):
    return dict((column.name, getattr(model, column.name))
        for column in model.__table__.columns)

"""
@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.filter(User.id==userid).first()
"""

"""
@app.route('/accounts/create', methods=["GET", "POST"])
def create_account():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User(
            email = form.email.data,
            password = form.password.data
        .session.add(user)
        db.session.commit()

        subject = "Confirm your email"
        token = ts.dumps(self.email, salt='email-confirm-key')
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('email/activate.html', confirm_url=confirm_url)
        send_email(user.email, subject, html)

        return redirect(url_for("index"))

    return render_template("accounts/create.html", form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('signin'))

@app.route('/')
def index():
    return render_template("index.html",recent_users=recent_users)
"""

@app.route('/login', methods=["GET", "POST"])
def login():
    form = UsernamePasswordForm()

    if form.validate_on_submit():
#        user = User.login(form.username.data, form.password.data)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user.is_correct_password(form.password.data):
            redis_store.set('username', request.form['username'])
#            login_user(user, form.remember_me.data)
            session['auth.user'] = get_model_dict(user) 
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
    redis_store.set('username', '')
    logout_user()
    session.clear()

    return redirect(url_for('.login'))

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = EmailPasswordForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('ユーザー登録が完了しました。ログインして下さい')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

"""
@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or+404()
        subject = "Password reset requested"
        token = ts.dumps(self.email, salt='recover-key')
        recover_url = url_for('reset_with_token', token=token, _external=True)
        html = render_template('email/recover.html', recover_url=recover_url)

        send_email(user.email, subject, html)
        return redirect(url_for('get_qiita'))
        
    return render_template('reset.html', form=form)

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('signin'))

    return render_template('reset_with_token.html', form=form, token=token)

@app.route('/dashboard')
@login_required
def account():
    return render_template("account.html")
"""

@app.route('/')
def get_qiita():
#    form = UsernamePasswordForm()

#    if form.validate_on_submit():
#        user = User.query.filter_by(username=form.username.data).first_or_404()
#        if user.is_correct_password(form.password.data):
#            redis_store.set('username', request.form['username'])

    if 'auth.user' is None:
        return redirect(url_for('.login')) 
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
    return render_template('index.html', articles=articles, user=redis_store.get('username'))
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

    return render_template('search_result.html', searched_result=searched_result, user=redis_store.get('username').decode("utf-8"))

"""
@app.route('/fav/<user>')
def favorite_qiita():
    fav = []
    if 'auth.user' in session:
        # ログインしているユーザーの記事だけを
        # 一覧で表示するようにしています
        fav = Fav.query.filter(Fav.user_id == session['auth.user']['id']).order_by(Fav.publish_date.desc()).all()

    return render_template('fav.html', form=form)
"""

if __name__ == '__main__':
        app.run(host='localhost',debug=True)

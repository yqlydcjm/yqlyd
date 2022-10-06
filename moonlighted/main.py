# coding=UTF-8
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField,RadioField
from wtforms.validators import DataRequired,Email
from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename
app = Flask(__name__, template_folder='templates')




app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '1317497275@qq.com' #邮箱账号
app.config['MAIL_PASSWORD'] = 'ibncvrjxtqmhbadj'  #QQ邮箱授权码              
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
parent = os.path.dirname(os.path.realpath(__file__))
#// 用户表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(36), nullable=True)
    username = db.Column(db.String(36), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=True)
    info = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(100), nullable=True)
    posts = db.relationship('Post', backref='author')
    shops = db.relationship('Shop', backref='author')
    blogs = db.relationship('Blog', backref='author')
#*  博客数据表
class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer(), primary_key=True)
    commodity = db.Column(db.String(100))
    content = db.Column(db.String(100))
    gender = db.Column(db.String(7))
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
# *商品数据表
class Shop(db.Model):
    __tablename__ = 'shops'
    id = db.Column(db.Integer(), primary_key=True)
    avatar = db.Column(db.String(100), nullable=True)# 商品图片
    commodity = db.Column(db.String(100))
    content = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
# *群聊数据表
class Post(db.Model):
    __tablename__ = 'newspaper'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
# *注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱:', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    confirm = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('立即注册')
# *登录表单
class LoginForm(FlaskForm):
    email = StringField('邮箱:', validators=[DataRequired()])
    password = PasswordField('密码:', validators=[DataRequired()])
    submit = SubmitField('登录')
# *修改个人信息表单
class DetailForm(FlaskForm):
    address = StringField('地址:')
    info = TextAreaField('个人简介:')
    submit = SubmitField('提交信息')
# *提交头像
class AvatarForm(FlaskForm):
    file = FileField("个人头像：", validators=\
        [FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('提交')
# *消息表单
class PostForm(FlaskForm):
    # content = TextAreaField('请输入内容;', validators=[DataRequired()])
    content = TextAreaField(id = 'content', validators=[DataRequired()])
    submit = SubmitField('发表')
# *提交商品且介绍
class ShopForm(FlaskForm):
    file = FileField("商品照片：", validators=\
        [FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif','bmp'])])
    commodity = StringField('商品名称:', validators=[DataRequired()])
    content = TextAreaField('介绍：', validators=[DataRequired()])
    contact = StringField('联系方式:', validators=[DataRequired()])
    submit = SubmitField('提交')
# class RadioForm(FlaskForm):
#     gender = RadioField(choices = [('Male','Male'),('Female','Female')])
#     submit = SubmitField('提交')
class RadioForm(FlaskForm):
    commodity = StringField('', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])
    gender = RadioField(choices = [('语文','语文'),('英语','英语'),('地理','地理'),('历史','历史'),('数学','数学'),('物理','物理'),('化学','化学'),('生物','生物'),('c++','c++'),('c#','c#'),('python','python'),('web前端','web前端'),('新闻','新闻'),('政治','政治')])
    submit = SubmitField('提交')
# *上下文处理器如果登录返回um如果没有返回空列表
@app.context_processor
def my_context_processor():
    email_id = session.get('email_id')
    if email_id:
        email = User.query.filter(User.id == email_id).first()
        if email:
            return {"um": email}
    return {}
@app.route('/a')
def a():
    return render_template('a.html')
# !学生管理系统
@app.route('/school')
def school():
    return render_template('school.html')
# *主页    
@app.route('/')
def zy():
    ab = Blog.query.all()
    for i in ab:
        global content
        content = i.content[0:70]+'.......'.replace('<br>','       ')# *切片0到100加上省略号把换行符变成空格
    shops = Shop.query.all()
    shops=shops[0:7]
    ab=ab[0:7]
    return render_template('zy.html', ab=ab,shops = shops)
# *博客主页
@app.route('/blog_sy')
def blog_sy():
    ab = Blog.query.all()
    return render_template('blog_sy.html', ab=ab)

# *博客页面
@app.route('/blog_ym/<ym>')
def blog_ym(ym):
    ab = Blog.query.filter(Blog.gender == ym).all()
    # !
    for i in ab:
        global content
        content = i.content[0:70]+'.......'.replace('<br>','       ')# *切片0到100加上省略号把换行符变成空格
    return render_template('blog_ym.html', ab=ab)
# *提交博客
@app.route('/blog_publish/', methods=['GET', 'POST'])
def blog_publish():
    if session.get('email_id'):
        form = RadioForm()
        if request.method == 'GET':
            return render_template('blog_publish.html', form=form)
        else:
            commodity = form.commodity.data
            content = form.content.data
            if content=='':
                content='请输入内容，三秒后返回'
                return render_template('zcdl.html',content=content,url=url_for('blog_publish'))
            gender = form.gender.data
            content = content.replace('\n','<br/>')
            new_user = Blog(commodity=commodity,content=content,gender=gender)
            new_user.author_id = session.get('email_id')
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('zy'))
    else:
        return redirect(url_for('dl'))
# *删除博客功能
@app.route('/delete_blog/<blog_id>', methods=['GET', 'POST'])
def delete_blog(blog_id):
    email_id = session.get('email_id')
    blog = Blog.query.filter(Blog.id == blog_id).first()
    if blog.author_id == email_id or '2556689087@qq.com' or'1317497275@qq.com':
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for('zy'))
    else:
        return "无权操作！"
# *博客文章
@app.route('/blog_page/<page_id>')
def blog_page(page_id):
    page = Blog.query.filter(Blog.id == page_id).first()
    return render_template('blog_page.html', page=page)

# *注册
@app.route('/zc', methods=['GET', 'POST'])
def zc():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('zc.html', form=form)
    else:
        email = form.email.data
        username = form.username.data
        password = form.password.data
        confirm = form.confirm.data
        if form.submit.data:
            prove = User.query.filter(User.email == email).first()
            if prove:
                content = "该邮箱已被注册！2秒后返回注册页面"
                return render_template('zcdl.html',content=content,url=url_for('zc'))
            else:
                if password != confirm:
                    content="密码不一致，请核对后填写！2秒后返回注册页面"
                    return render_template('zcdl.html',content=content,url=url_for('zc'))
                else:
                    new_user = User(username=username, password=password, email=email)
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for('dl'))
# *登录
@app.route('/dl', methods=['GET', 'POST'])
def dl():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('dl.html', form=form)
    else:
        # 获取用户输入的登录用户名
        email = form.email.data
        password = form.password.data

        email = User.query.filter(User.email == email).first()
        if email and password == email.password:
            session['email_id'] = email.id
            session.permanent = True
            content='登陆成功2秒后跳转至主页面'
            return redirect(url_for('zy'))
        else:
            content='用户名或密码错误2秒后返回登录页面'
            return render_template('zcdl.html',content=content,url=url_for('dl'))
# *退出登录
@app.route('/base_logout')
def base_logout():
    session.clear()
    return redirect(url_for('dl'))
# *购物
@app.route('/shop/')
def shop():

    shops = Shop.query.all()
    shops=shops[::-1] # !倒流
    return render_template('shop.html', shops=shops)
# *商品页面
@app.route('/shop_page/<shop_id>')
def shop_page(shop_id):
    shop = Shop.query.filter(Shop.id == shop_id).first()
    return render_template('shop_page.html',shop=shop)
# *删除商品界面
@app.route('/delete_shop/<shop_id>', methods=['GET', 'POST'])
def delete_shop(shop_id):
    email_id = session.get('email_id')
    shop = Shop.query.filter(Shop.id == shop_id).first()
    if shop.author_id == email_id or '2556689087@qq.com' or'1317497275@qq.com':
        os.remove(parent+shop.avatar)
        db.session.delete(shop)
        db.session.commit()
        return redirect(url_for('shop'))
    else:
        return "无权操作！"
# *发布商品
@app.route('/shop_publish', methods=['GET', 'POST'])
def shop_publish():
    b = session.get('email_id')
    if b:
        form = ShopForm()
        if request.method == 'GET':
            return render_template('shop_publish.html', form=form)
        else:
                f = request.files['file']
                commodity = form.commodity.data
                content = request.form["content"]
                contact = form.contact.data
                content = content.replace('\n','<br/>')
                filename = secure_filename(f.filename)#检查
                suffix = filename.split(".")[-1]#获取后缀
                file_rename = str\
                    (uuid.uuid4()) + "." + suffix#重命名防止遇到同名图片
                f.save(os.path.join(basedir, \
                    'static/shop/{}'.format(file_rename)))#保存到文件夹
                f.avatar = '/static/shop/{}'.format(file_rename)
                shop = Shop(avatar=f.avatar, commodity=commodity, content=content, contact=contact)
                shop.author_id = session.get('email_id')
                db.session.add(shop)
                db.session.commit()
                return redirect(url_for('shop'))
    else:
        return redirect(url_for('dl'))

# *个人资料
@app.route('/user_detail/<user_id>')
def user_detail(user_id):
    # !

    email = User.query.filter(User.id == user_id).first()
    blog = Blog.query.filter(Blog.author_id == user_id).all()
    shop = Shop.query.filter(Shop.author_id == user_id).all() 
    return render_template('user_detail.html', email=email, blog=blog, shop= shop)

# *修改头像
@app.route('/edit_avatar/<email_id>', methods=['POST', 'GET'])
def edit_avatar(email_id):
    if session.get('email_id') == int(email_id):
        form = AvatarForm()
        if request.method == 'GET':
            return render_template('edit_avatar.html', form=form)
        else:
            f = request.files['file']
            file_rename = str\
                (uuid.uuid4()) + "." + "jpg"#重命名防止遇到同名图片
            f.save(os.path.join(basedir, \
                'static/avatar/{}'.format(file_rename)))#保存到文件夹
            user = User.query.filter(User.id == email_id).first()
            user.avatar = '/static/avatar/{}'.format(file_rename)# 上传数据库
            db.session.commit()
            return redirect(url_for('zy'))
    else:
        return "您无权操作！"

# *修改个人简介
@app.route('/edit_info/<email_id>', methods=['GET', 'POST'])
def edit_info(email_id):
    if session.get('email_id') == int(email_id):
        form = DetailForm()
        if request.method == 'GET':
            return render_template('edit_info.html', form=form)
        else:
            email = User.query.filter(User.id == email_id).first()
            address = form.address.data
            info = form.info.data
            email.address = address
            email.info = info
            db.session.commit()# 提交会话
            return redirect(url_for('zy'))
    else:
        return "您无权操作！"
if __name__ == '__main__':
    # db.drop_all()# 删除数据表
    # db.create_all()# 创建数据表
    #app.run(host='0.0.0.0', port=80)
    app.run(debug=True)
#  ! 红色的高亮注释
#  ? 蓝色的高亮注释
#  * 绿色的高亮注释
#  todo 橙色的高亮注释
#  普通的注释
#  ! 红色的高亮注释
#  ? 蓝色的高亮注释
#  * 绿色的高亮注释
#  todo 橙色的高亮注释
# // 灰色带删除线的注释

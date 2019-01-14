#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-07 11:07:00
# @Author  : OP (oldpottertom@icloud.com)
# @Link    : https://shenkeling.top
# @Version : $Id$

from . import app, db
from flask import render_template, flash, redirect, url_for, request
from .forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('发布成功')
        return redirect(url_for('index'))
    # user = {'username': 'Tom'}
    # posts = [
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    page = request.args.get('page', 1, type=int)
    posts = current_user.following_post().paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='主页', posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #登录成功
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或者密码错误')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash('欢迎你:{}!'.format(form.username.data))
        return redirect(next_page)
    return render_template('login.html', title='登录', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你，注册成功！！')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册用户', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    '''
    个人主页
    :param username:
    :return:
    '''
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', page=posts.next_num, username=username) if posts.has_next else None
    prev_url = url_for('user', page=posts.prev_num, username=username) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=('GET', 'POST'))
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('更新已经保存成功！！')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='编辑', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('没找到用户:{}'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('你不能关注你自己')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('你成功关注了{}'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('没找到用户:{}'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('你不能取消关注你自己')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('你取消了对{}的关注'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='发现', posts=posts.items, next_url=next_url, prev_url=prev_url)


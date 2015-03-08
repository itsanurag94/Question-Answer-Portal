# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
@auth.requires_login()
def view_comment():
    no=request.args(0)
    c=db((db.comment1.pid==no)&(db.auth_user.id==db.comment1.author)).select()
    return dict(c=c,no=no)

@auth.requires_login()
def post_comment():
    c=request.args(0)
    form=SQLFORM.factory(
        Field('comment1_b','text'))
    if form.accepts(request.vars,session):
        db.comment1.insert(comment1_body=form.vars.comment1_b,pid=c)
        redirect(URL('view_comment',args=c))
    elif form.errors:
        response.flash="Error"
    return dict(form=form)
def index():
    rows=db(db.Blog_post).select()
    return locals()
@auth.requires_login()
def create():
    db.Blog_post.time_stamp.default=request.now
    db.Blog_post.time_stamp.writeable=False
    db.Blog_post.time_stamp.readable=False
    form=SQLFORM(db.Blog_post).process()
    if form.accepted:
        redirect(URL('index'))
    return locals()


def show():
    post=db.Blog_post(request.args(0,cast=int))
    return dict(post=post)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)

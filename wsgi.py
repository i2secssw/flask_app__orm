# -- coding: utf-8 --

from board_test import *

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "GET":
        if 'username' in session:
            return render_template('main.html')
        else:
            return render_template('login.html')
    elif request.method == "POST":
        u = get_user(fo('user_id'))
        if u.verify_login(fo('password')):
            session['username'] = u.user_id
            return redirect(url_for('main'))
        else:
            return alert_replace('잘못된 접근입니다!', '/')

@app.route('/welcome', methods=['GET','POST'])
def welcome():
    if request.method == "GET":
        return render_template('welcome.html')
    elif request.method == "POST":
        col = ['user_id','password','name','email','mobile']
        for name in col:
            if len(fo(name)) < 1:
                return alert_replace('공백이 있습니다!', '/welcome')
        user_add(fo('user_id') ,fo('password'),fo('name'),fo('email'),fo('mobile'))
        return alert_replace('{}님 환영합니다!'.format(fo('user_id')), '/')

@app.route('/secret', methods=['GET','POST'])
def secret():
    if 'username' in session:
        if request.method == "GET":
            u = get_user(session['username'])
            data=[u.user_id, u.password, u.name, u.email, u.mobile]
            return render_template('secret.html', data=data)
        elif request.method == "POST":
            data = check_space(['password','name','email','mobile'])
            user_update(session['username'], data['password'], data['name'], data['email'], data['mobile'])
            return redirect(url_for('main'))
    else:
        return alert_go('잘못된 접근입니다.',-1)

@app.route('/confirm',methods=['GET','POST'])
def confirm_pw():
    if 'username' in session:
        if request.method == 'GET':
             return render_template('confirm.html')
        elif request.method == 'POST':
             u = get_user(session['username'])
             if u.verify_login(fo('password')):
                 return redirect(url_for('secret'))
             else:
                 return alert_go('잘못된 접근입니다.',-1)
    else:
        return alert_replace('잘못된 접근입니다.',-1)

@app.route('/logout',methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        return alert_replace('다시 로그인하세요','/')
    else:
        return alert_replace('잘못된 접근입니다','/')

@app.route('/main', methods=['GET'])
def main():
    if 'username' in session:
        if request.method == "GET":
            return render_template('main.html',data=post_list())
    else:
        return alert_replace('잘못된 접근입니다.','/')

@app.route('/write', methods=['GET','POST'])
def post_write():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('write.html')
        elif request.method == 'POST':
            c = time.time()
            ct = datetime.datetime.fromtimestamp(c).strftime('%Y-%m-%d %H:%M:%S')
            for name in ['title','content']:
                if len(fo(name)) < 1:
                    return alert_replace('공백이 있습니다', '/write')
            write_post(fo('title'),fo('content'),session['username'], ct)
            return redirect(url_for('main'))
    else:
        return alert_replace('잘못된 접근입니다', '/')

@app.route('/main/del/<idx>', methods=['GET'])
def post_del(idx):
    if 'username' in session:
       delete_post(idx)
       return redirect(url_for('main'))
    else:
       return alert_go('권한이 없습니다', -1)

@app.route('/main/view/<idx>', methods=['GET'])
def post_view(idx):
    p = get_post(idx)
    print p
    data = [p.idx, p.title, p.content, p.writer, p.ctime]
    if session['username'] == p.writer:
        return render_template('view.html',data=data,perm=p.writer)
    else:
        return render_template('view.html',data=data,perm=None)

@app.route('/main/modi/<idx>',methods=['GET','POST'])
def post_modify(idx):
    if 'username' in session:
        if request.method == 'GET':
            p = get_post(idx)
            data = [p.idx, p.title, p.content, p.writer, p.ctime]
            return render_template('modi.html',data=data)
        elif request.method == 'POST':
            cdata = check_space(['title','content'])
            modify_post(idx, cdata['title'], cdata['content'])
            return redirect(url_for('main'))
    else:
        return alert_replace('권한이 없습니다','/')

#helper function
def fo(col):
    return request.form.get(col)

def alert_replace(msg, loc):
    return "<script>alert('{}'); location.replace('{}');</script>".format(msg, loc)

def alert_go(msg,loc):
    return "<script>alert('{}'); hitory.go({});</script>".format(msg, loc)

def check_space(data):
    r = dict()
    for name in data:
        if len(fo(name)) < 1:
             r[name] = None
        else:
             r[name] = fo(name)
    return r

if __name__ == "__main__":
#    db.drop_all()
#    db.create_all()
    app.run(host='0.0.0.0', port=5000)

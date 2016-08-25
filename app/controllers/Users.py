
from system.core.controller import *
from flask import Flask,flash

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Message')
        self.db = self._app.db

    """ GET ROUTES """

    def index(self):
        return self.load_view('index.html')

    def login(self):
        return self.load_view('login.html')

    def register(self):
        return self.load_view('register.html')

    def dashboard(self):
        users = self.models['User'].get_users()
        return self.load_view('dashboard.html',users=users)

    def show(self,id):
        user = self.models['User'].get_user(id)
        messages = self.models['Message'].get_messages(id)
        comments = self.models['Message'].get_comments(id)
        return self.load_view('show.html',user=user[0],messages=messages,comments=comments)

    def new(self):
        return self.load_view('new.html')

    def edit(self,id):
        user = self.models['User'].get_user(id)
        return self.load_view('edit.html',user=user[0])

    def logout(self):
        session.clear()
        return redirect('/')

    def delete(self,id):
        user = self.models['User'].get_user(id)
        return self.load_view('delete.html',user=user[0])

    def destroy(self,id):
        data = {"id":id}
        user = self.models['User'].destroy_user(id)
        flash('User deleted!')
        return redirect('/dashboard')

    """ POST ROUTES """

    def proccess_login(self):
        data = request.form
        user = self.models['User'].login_user(data)
        if not user:
            flash("Your login information is incorrect. Please try again.")
            return redirect('/login')
        session['id'] = user[0]['id']
        session['user_level'] = user[0]['user_level']
        flash("You have successfully signed in!")
        return redirect('/dashboard')

    def process_register(self):
        create_status = self.models['User'].create_user(request.form)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['user_level'] = create_status['user']['user_level']
            flash('You have successfully registered!')
            return redirect('/dashboard')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/register')

    def new_user(self):
        valid = self.models['User'].create_user(request.form)
        if valid == True:
            return redirect('/dashboard')
        else:
            return redirect('/users/new')

    def edit_information(self):
        # add validation
        user = self.models['User'].update_user(request.form)
        flash('Information updated!')
        return redirect('users/show/{}'.format(request.form['id']))

    def edit_password(self):
        # add validation
        user = self.models['User'].update_user(request.form)
        flash('Password updated!')
        return redirect('users/show/{}'.format(request.form['id']))

    def edit_description(self):
        user = self.models['User'].update_user(request.form)
        flash('Description updated!')
        return redirect('users/show/{}'.format(request.form['id']))

    def new_message(self):
        message = self.models['Message'].add_message(request.form)
        flash('Message posted!')
        return redirect('users/show/{}'.format(request.form['wall_id']))

    def new_comment(self):
        comment = self.models['Message'].add_comment(request.form)
        flash('Comment posted!')
        return redirect('users/show/{}'.format(request.form['wall_id']))

    def delete_message(self,message_id):
        message = self.models['Message'].destroy_message(message_id)
        flash('Message deleted!')
        return redirect('users/show/{}'.format(request.form['wall_id']))

    def delete_comment(self,comment_id):
        comment = self.models['Message'].destroy_comment(comment_id)
        flash('Comment deleted!')
        return redirect('users/show/{}'.format(request.form['wall_id']))


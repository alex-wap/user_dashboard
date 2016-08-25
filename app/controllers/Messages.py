
from system.core.controller import *
from flask import Flask,flash

class Messages(Controller):
    def __init__(self, action):
        super(Messages, self).__init__(action)
        self.load_model('User')
        self.load_model('Message')
        self.db = self._app.db

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


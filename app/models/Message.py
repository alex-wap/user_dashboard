from system.core.model import Model

class Message(Model):
    def __init__(self):
        super(Message, self).__init__()

    def get_messages(self,id):
        query = '''SELECT user_id,wall_id,first_name,last_name,messages.created_at,message,messages.id 
                    FROM messages JOIN users ON users.id = messages.user_id 
                    WHERE wall_id=:id
                    ORDER BY messages.created_at DESC'''
        data = {'id': id}
        return self.db.query_db(query, data)

    def add_message(self,data):
        print data
        sql = "INSERT INTO messages (message, created_at, user_id, wall_id) values(:message, NOW(), :id, :wall_id)"
        self.db.query_db(sql, data)
        return True

    def get_comments(self,id):
        query = '''SELECT first_name,last_name,messages.id as message_id,messages.user_id,comments.comment,comments.created_at,comments.user_id,messages.wall_id,comments.id FROM users
                    JOIN messages ON users.id=messages.user_id
                    JOIN comments ON messages.id=comments.message_id'''
        data = {'id': id}
        return self.db.query_db(query, data)

    def add_comment(self,data):
        print data
        sql = "INSERT INTO comments (comment, created_at, user_id, message_id, wall_id) values(:comment, NOW(), :id, :message_id, :wall_id)"
        self.db.query_db(sql, data)
        return True

    def destroy_message(self,message_id):
        query_comments = "DELETE FROM comments where message_id = :id"
        data = {"id" : message_id }
        self.db.query_db(query_comments,data)
        query_message = "DELETE FROM messages where id = :id LIMIT 1"
        self.db.query_db(query_message,data)
        return True

    def destroy_comment(self,comment_id):
        query = "DELETE FROM comments where id = :id LIMIT 1"
        data = {"id" : comment_id }
        self.db.query_db(query,data)
        return True
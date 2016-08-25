from system.core.router import routes

# GET routes
routes['default_controller'] = 'Users'
routes['/login'] = 'Users#login'
routes['/register'] = 'Users#register'
routes['/dashboard'] = 'Users#dashboard'
routes['/users/show/<id>'] = 'Users#show'
routes['/users/new'] = 'Users#new'
routes['/users/edit/<id>'] = 'Users#edit'
routes['/users/delete/<id>'] = 'Users#delete'
routes['/users/destroy/<id>'] = 'Users#destroy'
routes['/logout'] = 'Users#logout'


# POST routes
routes['POST']['/process_login'] = 'Users#proccess_login'
routes['POST']['/process_register'] = 'Users#process_register'
routes['POST']['/users/new_user'] = 'Users#new_user'
routes['POST']['/users/edit_information'] = 'Users#edit_information'
routes['POST']['/users/edit_password'] = 'Users#edit_password'
routes['POST']['/users/edit_description'] = 'Users#edit_description'

# Messages controller routes
routes['POST']['/new_message'] = 'Messages#new_message'
routes['POST']['/new_comment'] = 'Messages#new_comment'
routes['POST']['/message/destroy/<message_id>'] = 'Messages#delete_message'
routes['POST']['/comment/destroy/<comment_id>'] = 'Messages#delete_comment'


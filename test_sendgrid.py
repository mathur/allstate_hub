import sendgrid

sg = sendgrid.SendGridClient('mathur', 'lolallstate222')

message = sendgrid.Mail(to='rohanmathur34@gmail.com', subject='Hello', html='hello', text='hello', from_email='hub@allstate.com')
status, msg = sg.send(message)
print status
print msg
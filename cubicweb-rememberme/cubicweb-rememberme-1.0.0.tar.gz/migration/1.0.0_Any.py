rql('DELETE CWAuthCookie C')
commit()
drop_attribute('CWAuthCookie', 'magicnumber')
add_attribute('CWAuthCookie', 'magic')

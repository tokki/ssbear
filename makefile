.PHONY : css account

css: 
	stylus -w static/css/app.styl -u nib

account:
	stylus -w static/css/account.styl -u nib





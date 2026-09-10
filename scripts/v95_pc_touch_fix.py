from pathlib import Path
p=Path('app-v9-5.html')
s=p.read_text()
css='''\n<style>\n@media (min-width:1200px){\n body.device-pc:not(.d12-auth-mode) .btn,body.device-desktop:not(.d12-auth-mode) .btn{min-height:48px!important;padding-top:10px!important;padding-bottom:10px!important}\n}\n</style>\n'''
s=s.replace('</head>',css+'</head>',1)
p.write_text(s)
print('Applied Version 9.5 PC touch-target fix')

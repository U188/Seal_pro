import sendNotify,os
title=os.environ["title"]
msg=os.environ["msg"]
sendNotify.send(title,msg)
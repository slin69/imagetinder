from flask import *
from flask import *

import base64
import random
from werkzeug.utils import secure_filename
import json
from flask_login import login_required, current_user
from .models import User,Image
from . import db



bp=Blueprint('views',__name__,url_prefix='/')
@bp.route("/",methods=["POST","GET"])
@login_required
def home():
    if request.method == 'POST':
        pic=request.files['pic']
        if not pic:
            return 'no pic',400
        filename=secure_filename(pic.filename)
        mimetype=pic.mimetype
        if not filename or not mimetype:
            return 'bad image',400
        img=Image(image=pic.read(),name=filename,mimetype=mimetype,likes=0,user_id=current_user.id)

        db.session.add(img)
        db.session.commit()
    return render_template("index.html")

@bp.route(f'/image')
def get_img():
    images=[]
    obs=[]
    size=len(Image.query.filter_by().all())
    for  i in range(2):
        i=random.randint(1,size)
        #id=random.randint(1,2)
        file_data = Image.query.filter_by(id=i).first()
        image = base64.b64encode(file_data.image).decode('ascii')
        images.append(image)
        obs.append(file_data)
    for e in range(len(images)):
        print(obs[e].likes)
        



    return render_template("image.html",r=images,f=obs)
@bp.route("/like",methods=["POST","GET"])
def like():
    c1=json.loads(request.data)
    c1a=c1['n']
    if c1:
        print("c1",c1a)
        i=Image.query.filter_by(id=c1a).first()
        i.likes+=1
        print(i.likes)
        db.session.commit()

    else:
        print("no")
    return jsonify({})


@bp.route("/dislike",methods=["POST","GET"])
def dislike():
    c1=json.loads(request.data)
    c1a=c1['n']
    if c1:
        print("c1",c1a)
        i=Image.query.filter_by(id=c1a).first()
        i.likes-=1
        print(i.likes)
        db.session.commit()

    else:
        print("no")
    return jsonify({})
@bp.route("/myimage")
def myimage():
    images=[]
    image=Image.query.filter_by(user_id=current_user.id).all()
    for i in range(len(image)):
        idata=base64.b64encode(image[i].image).decode('ascii')
        images.append(idata)
    
    


    return render_template("myimage.html",user=current_user,i=images,n=image)
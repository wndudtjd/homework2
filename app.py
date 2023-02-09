from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.3lyvfuj.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/homework2", methods=["POST"])
def homework2_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    comment_list = list(db.homework2.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'num': count
    }
    db.homework2.insert_one(doc)
    return jsonify({'msg':'응원 완료!'})

@app.route("/homework2", methods=["GET"])
def homework2_get():
    comment_list = list(db.homework2.find({}, {'_id': False}))
    return jsonify({'comments':comment_list})

# modify(수정 기능!!)
@app.route("/homework2/modify", methods=["POST"])
def modify_comment_post():
    comment_receive = request.form['comment_give']
    num_receive = request.form['num_give']
    print(comment_receive,num_receive)
    db.homework2.update_one({'num': int(num_receive)}, {'$set': {'comment': comment_receive}})
    return jsonify({'msg':'수정 완료!'})

# delete(삭제 기능!!)
@app.route("/homework2/delete", methods=["POST"])
def delete_post():
    num_receive = request.form['num_give']
    db.homework2.delete_one({'num': int(num_receive)})
    return jsonify({'result': 'success','msg':'삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
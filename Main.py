from flask import Flask, request, send_file;
from flaskext.mysql import MySQL;
import json;

UPLOAD_FOLDER = "/Users/Henry/Documents/nextagram_server/image/"

app = Flask(__name__);
mysql = MySQL();

app.config['MYSQL_DATABASE_USER'] = 'root';
app.config['MYSQL_DATABASE_PASSWORD'] = 'db1004';
app.config['MYSQL_DATABASE_DB'] = 'DBHW';

mysql.init_app(app);

@app.route("/")
def helloWorld():
	return "helloWorld";

@app.route("/loadComment", methods=["GET", "POST"])
def loadComment():
	cursor = mysql.connect().cursor();
	cursor.execute("select * from nextagram_comment");

	result = []
	columns = tuple( [d[0] for d in cursor.description])

	for row in cursor:
		result.append(dict(zip(columns,row)))

	return json.dumps(result);

@app.route("/loadData", methods=["GET", "POST"])
def loadData():
	cursor = mysql.connect().cursor();
	cursor.execute("select * from next_android_nextagram");

	result = []
	columns = tuple( [d[0] for d in cursor.description])

	for row in cursor:
		result.append(dict(zip(columns,row)))
			

	return json.dumps(result);

@app.route("/deleteComment", methods=["POST"])
def deleteComment():
	if request.method == 'POST':
		articleNumber = request.form['articleNumber']
		commentNumber = request.form['commentNumber']

		con = mysql.connect();
		cursor = con.cursor();

		query = "delete from nextagram_comment \
					where ArticleNumber=" + articleNumber + " and CommentNumber=" + commentNumber +";"

		cursor.execute(query);
		con.commit();

		return "ok";

@app.route("/uploadComment", methods=["POST"])
def uploadComment():
	if request.method == 'POST':
		articleNumber = request.form['articleNumber']
		commentWriter = request.form['commentWriter']
		commentDate = request.form['commentDate']
		comment = request.form['comment']

		con = mysql.connect();
		cursor = con.cursor();

		query = "insert into nextagram_comment \
		(ArticleNumber, CommentWriter, CommentDate, Comment) values \
		(" + articleNumber + ", '" + commentWriter + "', '" + commentDate + "', '" + comment + "');";

		cursor.execute(query);
		con.commit();

		return "ok";


@app.route("/upload", methods=["POST"])
def upload():
	if request.method == 'POST':
		title = request.form['title']
		writer = request.form['writer']
		id = request.form['id']
		content = request.form['content']
		writeDate = request.form['writeDate']
		imgName = request.form['imgName']
		
		file = request.files['uploadedfile']
		path = UPLOAD_FOLDER + file.filename;

		if file and allowed_file(file.filename):
			file.save(path)
			
			con = mysql.connect();
			cursor = con.cursor();

			query = "insert into next_android_nextagram \
			(Title, Writer, Id, Content, WriteDate, ImgName) values \
			('" + title + "', '" + writer + "', '" + id + "', '" + content + "', \
				'" + writeDate + "', '" + imgName + "');";

			cursor.execute(query);
			con.commit();

			return "ok";

	return "error";

@app.route("/image/<fileName>", methods=["GET", "POST"])
def loadImage(fileName):
	print("fileName:" + fileName);
	return send_file(UPLOAD_FOLDER + fileName, mimetype='image');

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']);
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS;


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5009);
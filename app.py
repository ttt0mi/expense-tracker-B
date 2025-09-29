from configurations.app_config import create_app

app = create_app(__name__)

@app.route('/')
def hello_world():
	return 'OG, how far!'


if __name__ == '__main__':
	app.run(debug=True)